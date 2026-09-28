from rest_framework import generics

class GeneralListarAPIView(generics.ListAPIView):
    serializer_class = None

    def get_queryset(self):
        model = self.serializer_class.Meta.model
        return model.objects.filter(estado=True)