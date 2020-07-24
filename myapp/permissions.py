from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsTeacher(BasePermission):
    message = "You must be a Teacher to view all the doubts."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_teacher

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_teacher

class IsStudent(BasePermission):
    message = "You must be a student to ask doubts."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_student

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_student