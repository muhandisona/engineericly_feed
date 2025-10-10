from unfold.widgets import UnfoldAdminImageFieldWidget

class CustomUnfoldAdminImageFieldWidget(UnfoldAdminImageFieldWidget):
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["attrs"]["accept"] = 'image/*'
        return context