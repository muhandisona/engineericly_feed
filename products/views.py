from pprint import pprint
from urllib.parse import urlparse

from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage
from django.utils import timezone

from .models import PostLink
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
    """API endpoint to get post links as JSON with domain-based filtering"""
    try:
        # Get and validate page parameter
        try:
            page = int(request.GET.get('page', 1))
        except ValueError:
            page = 1

        # Determine domain (query param > referrer > origin > host)
        domain = request.GET.get('domain')
        if not domain:
            domain = (
                request.META.get('HTTP_REFERER')
                or request.META.get('HTTP_ORIGIN')
                or request.META.get('HTTP_HOST')
                or ''
            )

        # Extract only the hostname (e.g., instagram.com)
        parsed = urlparse(domain)
        hostname = parsed.hostname or domain.lower()

        # Filter post links by publish time
        now = timezone.now()
        post_links = PostLink.objects.filter(
            Q(published_at__isnull=True) | Q(published_at__lte=now)
        )

        # Domain-specific filtering
        if hostname:
            domain_lower = hostname.lower()
            if 'instagram' in domain_lower:
                post_links = post_links.filter(show_for_instagram=True)
            elif 'youtube' in domain_lower or 'youtu.be' in domain_lower:
                post_links = post_links.filter(show_for_youtube=True)
            elif 'tiktok' in domain_lower:
                post_links = post_links.filter(show_for_tiktok=True)
            # else: show all

        # Apply model-defined ordering
        # (This automatically uses Meta.ordering: ['-is_pinned', '-order', '-published_at'])

        # Paginate results
        paginator = Paginator(post_links, 12)
        try:
            page_obj = paginator.page(page)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        # Prepare response data
        items = [
            {
                'id': p.id,
                'title': p.title,
                'link': p.link,
                'file_link': p.file.url if p.file else '',
                'show_for_youtube': p.show_for_youtube,
                'show_for_tiktok': p.show_for_tiktok,
                'show_for_instagram': p.show_for_instagram,
                'is_pinned': p.is_pinned,
                'created_at': p.created_at.isoformat(),
                'updated_at': p.updated_at.isoformat(),
            }
            for p in page_obj
        ]

        response_data = {
            'items': items,
            'page': page_obj.number,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'total_pages': paginator.num_pages,
            'total_items': paginator.count,
        }

        return JsonResponse(response_data)

    except Exception as e:
        return JsonResponse(
            {'error': 'Failed to fetch post links', 'details': str(e)},
            status=500,
        )
