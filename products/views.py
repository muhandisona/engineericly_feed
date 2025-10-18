from pprint import pprint

from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone

from .models import Product
import json

def feed_view(request):
    """Main feed page view"""
    # Get domain information for debugging
    referrer = request.META.get('HTTP_REFERER', '')
    origin = request.META.get('HTTP_ORIGIN', '')
    host = request.META.get('HTTP_HOST', '')
    
    context = {
        'referrer': referrer,
        'origin': origin,
        'host': host,
    }
    
    return render(request, 'feed.html', context)

def api_gallery_view(request):
    """API endpoint to get products as JSON with domain-based filtering"""
    try:
        # Get page parameter, default to 1
        page = int(request.GET.get('page', 1))
        
        # Get domain from referrer, origin, host header, or query parameter (for testing)
        domain = request.GET.get('domain')  # Allow manual domain override for testing
        
        if not domain:
            referrer = request.META.get('HTTP_REFERER', '')
            origin = request.META.get('HTTP_ORIGIN', '')
            host = request.META.get('HTTP_HOST', '')
            
            # Check referrer first, then origin, then host
            if referrer:
                domain = referrer
            elif origin:
                domain = origin
            elif host:
                domain = host
        
        # Start with all products
        now = timezone.now()
        products = Product.objects.filter(
            Q(published_at__isnull=True) | Q(published_at__lte=now)
        )
        
        # Filter based on domain
        if domain:
            domain_lower = domain.lower()
            
            if 'instagram' in domain_lower:
                # Show only products marked for Instagram
                products = products.filter(show_for_instagram=True)
            elif 'youtube' in domain_lower or 'youtu.be' in domain_lower:
                # Show only products marked for YouTube
                products = products.filter(show_for_youtube=True)
            elif 'tiktok' in domain_lower:
                # Show only products marked for TikTok
                products = products.filter(show_for_tiktok=True)
            # If domain doesn't match any known platform, show all products
        
        # Order by pinned status and creation date
        products = products.order_by('-is_pinned', '-created_at')
        
        # Paginate results
        paginator = Paginator(products, 12)  # 12 items per page
        page_obj = paginator.get_page(page)
        
        # Prepare response data
        items = []
        for product in page_obj:
            items.append({
                'id': product.id,
                'title': product.title,
                'link': product.link,
                'file_link': product.file.url if product.file else '',
                'show_for_youtube': product.show_for_youtube,
                'show_for_tiktok': product.show_for_tiktok,
                'show_for_instagram': product.show_for_instagram,
                'is_pinned': product.is_pinned,
                'created_at': product.created_at.isoformat(),
                'updated_at': product.updated_at.isoformat(),
            })
        pprint(items)
        response_data = {
            'items': items,
            'page': page,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'total_pages': paginator.num_pages,
            'total_items': paginator.count,
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        return JsonResponse({
            'error': 'Failed to fetch products',
            'details': str(e)
        }, status=500)
