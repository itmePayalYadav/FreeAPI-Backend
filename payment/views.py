from rest_framework import generics, permissions, status
from django.conf import settings
from subscription.models import SubscriptionPlan
from .models import Payment
from .serializers import PaymentSerializer
from core.utils import api_success, api_error
from accounts.permissions import IsAdminUser, IsAuthenticatedUser, IsPremiumUser
import razorpay
import stripe

# -----------------------
# Clients setup
# -----------------------
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
stripe.api_key = settings.STRIPE_SECRET_KEY


# ==========================================
# USER PAYMENT LIST
# ==========================================
class UserPaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticatedUser]
    search_fields = ["subscription__name", "payment_method", "status"]
    ordering_fields = ["amount", "created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = Payment.objects.filter(user=self.request.user)
        status_filter = self.request.query_params.get("status")
        method_filter = self.request.query_params.get("payment_method")

        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if method_filter:
            queryset = queryset.filter(payment_method=method_filter)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return api_success(data=serializer.data, message="User payment list fetched successfully")


# ==========================================
# ADMIN PAYMENT LIST
# ==========================================
class AdminPaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminUser]
    
    search_fields = ["user__username", "subscription__name", "payment_method", "status"]
    ordering_fields = ["amount", "created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = Payment.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return api_success(data=serializer.data, message="Admin payment list fetched successfully")


# ==========================================
# ADMIN PAYMENT DETAIL
# ==========================================
class AdminPaymentDetailView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminUser]
    queryset = Payment.objects.all()

    def retrieve(self, request, *args, **kwargs):
        payment = self.get_object()
        serializer = self.get_serializer(payment)
        return api_success(data=serializer.data, message="Payment detail retrieved successfully")


# ==========================================
# ADMIN UPDATE PAYMENT STATUS
# ==========================================
class AdminPaymentUpdateStatusView(generics.RetrieveUpdateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminUser]
    queryset = Payment.objects.all()

    def patch(self, request, *args, **kwargs):
        payment = self.get_object()
        new_status = request.data.get("status")
        valid_status = [choice[0] for choice in payment._meta.get_field("status").choices]

        if new_status not in valid_status:
            return api_error(message="Invalid status value")

        payment.update_status(new_status)
        serializer = self.get_serializer(payment)
        return api_success(data=serializer.data, message=f"Payment status updated to {new_status}")


# ==========================================
# ADMIN DELETE PAYMENT
# ==========================================
class AdminPaymentDeleteView(generics.DestroyAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminUser]
    queryset = Payment.objects.all()

    def delete(self, request, *args, **kwargs):
        payment = self.get_object()
        payment.delete()
        return api_success(message="Payment deleted successfully", status_code=status.HTTP_204_NO_CONTENT)


# ==========================================
# CREATE PAYMENT
# ==========================================
class CreatePaymentView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticatedUser]

    def post(self, request, *args, **kwargs):
        user = request.user
        subscription_id = request.data.get("subscription_id")
        payment_method = request.data.get("payment_method")

        if not subscription_id or not payment_method:
            return api_error(message="subscription_id and payment_method are required")

        try:
            subscription = SubscriptionPlan.objects.get(id=subscription_id)
        except SubscriptionPlan.DoesNotExist:
            return api_error(message="Subscription plan not found", status_code=404)

        amount = subscription.price
        payment = Payment.objects.create(
            user=user,
            subscription=subscription,
            amount=amount,
            payment_method=payment_method
        )

        # ----- Razorpay -----
        if payment_method == "razorpay":
            try:
                order = razorpay_client.order.create({
                    "amount": int(amount * 100),
                    "currency": "INR",
                    "receipt": str(payment.transaction_id),
                    "payment_capture": 1
                })
                payment.metadata = {"razorpay_order_id": order["id"]}
                payment.save()
                return api_success(
                    data={
                        "transaction_id": str(payment.transaction_id),
                        "order_id": order["id"],
                        "amount": amount
                    },
                    message="Razorpay payment order created successfully"
                )
            except Exception as e:
                return api_error(message=f"Razorpay error: {str(e)}")

        # ----- Stripe -----
        elif payment_method == "stripe":
            try:
                intent = stripe.PaymentIntent.create(
                    amount=int(amount * 100),
                    currency="INR",
                    metadata={"transaction_id": str(payment.transaction_id)}
                )
                payment.metadata = {"stripe_payment_intent": intent["id"]}
                payment.save()
                return api_success(
                    data={
                        "transaction_id": str(payment.transaction_id),
                        "client_secret": intent["client_secret"],
                        "amount": amount
                    },
                    message="Stripe payment intent created successfully"
                )
            except Exception as e:
                return api_error(message=f"Stripe error: {str(e)}")

        return api_error(message="Invalid payment method")


# ==========================================
# VERIFY PAYMENT
# ==========================================
class VerifyPaymentView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedUser]

    def post(self, request, *args, **kwargs):
        transaction_id = request.data.get("transaction_id")
        payment_id = request.data.get("payment_id")
        signature = request.data.get("razorpay_signature")

        if not transaction_id or not payment_id:
            return api_error(message="transaction_id and payment_id are required")

        try:
            payment = Payment.objects.get(transaction_id=transaction_id)
        except Payment.DoesNotExist:
            return api_error(message="Payment not found", status_code=404)

        if payment.payment_method == "razorpay":
            try:
                razorpay_client.utility.verify_payment_signature({
                    "razorpay_order_id": payment.metadata.get("razorpay_order_id"),
                    "razorpay_payment_id": payment_id,
                    "razorpay_signature": signature,
                })
                payment.update_status("completed")
                return api_success(message="Razorpay payment verified successfully")
            except razorpay.errors.SignatureVerificationError:
                payment.update_status("failed")
                return api_error(message="Razorpay signature verification failed")

        elif payment.payment_method == "stripe":
            try:
                intent = stripe.PaymentIntent.retrieve(payment_id)
                payment.update_status("completed" if intent.status == "succeeded" else "failed")
                if payment.status == "completed":
                    return api_success(message="Stripe payment verified successfully")
                else:
                    return api_error(message="Stripe payment failed")
            except Exception as e:
                return api_error(message=f"Stripe verification error: {str(e)}")

        return api_error(message="Invalid payment method")
