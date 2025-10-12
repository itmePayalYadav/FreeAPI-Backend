import json
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve
from management.models import Subscription, Usage, Endpoint

class APILoggingMiddleware(MiddlewareMixin):
    """
    Middleware to automatically create a subscription and log API usage
    for authenticated users accessing valid API endpoints.
    """
    def process_response(self, request, response):
        user = getattr(request, "user", None)

        # Only log for authenticated users
        if not user or not user.is_authenticated:
            return response

        # Only log API endpoints
        if not request.path.startswith("/api/"):
            return response

        try:
            # Resolve URL kwargs (like slug)
            match = resolve(request.path)
            slug = match.kwargs.get("slug")

            endpoint_instance = None
            if slug:
                endpoint_instance = Endpoint.objects.filter(slug=slug, is_deleted=False).first()
            if not endpoint_instance:
                endpoint_instance = Endpoint.objects.filter(url__icontains=request.path, is_deleted=False).first()
            if not endpoint_instance:
                return response

            # Get or create a subscription
            subscription, created = Subscription.objects.get_or_create(
                user=user,
                api=endpoint_instance
            )

            # Safely parse request body
            try:
                body_data = json.loads(request.body.decode("utf-8")) if request.body else {}
            except Exception:
                body_data = {}

            # Query params
            query_data = request.GET.dict() if request.GET else {}

            # Log the API usage
            Usage.objects.create(
                subscription=subscription,
                status_code=response.status_code,
                method=request.method,
                request_body=body_data,
                query_params=query_data
            )

            # Increment usage count on subscription
            subscription.usage_count += 1
            subscription.save(update_fields=['usage_count'])

        except Exception as e:
            # Fail silently; logging only
            print(f"[APILoggingMiddleware] Failed to log API usage: {e}")

        return response
