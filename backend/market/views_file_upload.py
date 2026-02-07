from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Crop, CropDocument, User
from .serializers import CropSerializer, CropDocumentSerializer
from .permissions import IsOwnerOrReadOnly, IsFarmer

class CropDocumentViewSet(viewsets.ModelViewSet):
    serializer_class = CropDocumentSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['crop']

    def get_queryset(self):
        queryset = CropDocument.objects.all()
        crop_id = self.request.query_params.get('crop')
        if crop_id:
            queryset = queryset.filter(crop_id=crop_id)
        return queryset

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsFarmer]
        return super().get_permissions()

    def perform_create(self, serializer):
        crop_id = self.request.data.get('crop')
        if crop_id:
            crop = Crop.objects.get(id=crop_id)
            # Check if user owns the crop
            if crop.farmer == self.request.user or self.request.user.role == 'admin':
                serializer.save(crop=crop)
            else:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("You don't have permission to add documents to this crop.")
        else:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Crop ID is required.")

    @action(detail=True, methods=['delete'])
    def bulk_delete(self, request, pk=None):
        """
        Bulk delete documents for a crop
        """
        document_ids = request.data.get('document_ids', [])
        if not document_ids:
            return Response(
                {'error': 'No document IDs provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        documents = CropDocument.objects.filter(
            id__in=document_ids,
            crop__farmer=request.user
        )
        
        count = documents.count()
        documents.delete()
        
        return Response({
            'message': f'Successfully deleted {count} documents'
        })

class CropImageViewSet(viewsets.ViewSet):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated, IsFarmer]

    @action(detail=True, methods=['post'])
    def upload_image(self, request, pk=None):
        """
        Upload image for a crop
        """
        try:
            crop = Crop.objects.get(pk=pk)
            
            # Check ownership
            if crop.farmer != request.user and request.user.role != 'admin':
                return Response(
                    {'error': 'You do not have permission to upload images to this crop'},
                    status=status.HTTP_403_FORBIDDEN
                )

            if 'image' not in request.FILES:
                return Response(
                    {'error': 'No image file provided'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            image_file = request.FILES['image']
            
            # Validate file type
            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            if image_file.content_type not in allowed_types:
                return Response(
                    {'error': 'Invalid file type. Only JPEG, PNG, GIF, and WebP are allowed.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validate file size (max 5MB)
            if image_file.size > 5 * 1024 * 1024:
                return Response(
                    {'error': 'File too large. Maximum size is 5MB.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Delete old image if exists
            if crop.image:
                crop.image.delete()

            crop.image = image_file
            crop.save()

            serializer = CropSerializer(crop, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Crop.DoesNotExist:
            return Response(
                {'error': 'Crop not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['delete'])
    def delete_image(self, request, pk=None):
        """
        Delete crop image
        """
        try:
            crop = Crop.objects.get(pk=pk)
            
            # Check ownership
            if crop.farmer != request.user and request.user.role != 'admin':
                return Response(
                    {'error': 'You do not have permission to delete images from this crop'},
                    status=status.HTTP_403_FORBIDDEN
                )

            if crop.image:
                crop.image.delete()
                crop.image = None
                crop.save()

            return Response(
                {'message': 'Image deleted successfully'},
                status=status.HTTP_200_OK
            )

        except Crop.DoesNotExist:
            return Response(
                {'error': 'Crop not found'},
                status=status.HTTP_404_NOT_FOUND
            )

class UserProfileImageViewSet(viewsets.ViewSet):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def upload_profile_image(self, request):
        """
        Upload profile image for the authenticated user
        """
        if 'profile_image' not in request.FILES:
            return Response(
                {'error': 'No image file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        image_file = request.FILES['profile_image']
        
        # Validate file type
        allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        if image_file.content_type not in allowed_types:
            return Response(
                {'error': 'Invalid file type. Only JPEG, PNG, GIF, and WebP are allowed.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate file size (max 2MB)
        if image_file.size > 2 * 1024 * 1024:
            return Response(
                {'error': 'File too large. Maximum size is 2MB.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user
        
        # Delete old profile image if exists
        if user.profile_image:
            user.profile_image.delete()

        user.profile_image = image_file
        user.save()

        from .serializers import UserSerializer
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'])
    def delete_profile_image(self, request):
        """
        Delete profile image for the authenticated user
        """
        user = request.user
        
        if user.profile_image:
            user.profile_image.delete()
            user.profile_image = None
            user.save()

        from .serializers import UserSerializer
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
