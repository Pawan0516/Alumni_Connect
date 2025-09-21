from rest_framework import viewsets
from .models import College
from .serializers import CollegeSerializer
from .permissions import IsCollegeAuthority

class CollegeViewSet(viewsets.APIViewSet):
    queryset = College.objects.filter(is_deleted=False).order_by("-created_at")
    serializer_class = CollegeSerializer
    permission_classes = [IsCollegeAuthority]

    def perform_create(self, serializer):
        # Auto-assign logged-in user as admin
        serializer.save(admin=self.request.user)
