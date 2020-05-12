from rest_framework.serializers import ModelSerializer, SerializerMethodField, HyperlinkedIdentityField, \
    HyperlinkedModelSerializer, ReadOnlyField

from accounts.api.serializers import UserSerializer
from advertisements.models import Advertisement, AdvertisementImage, AdvertisementFollowing


class AdsListSerializer(ModelSerializer):
    author = SerializerMethodField('get_author_details')
    # url = HyperlinkedIdentityField(view_name='ad-api-detail')

    def get_author_details(self, obj):
        return UserSerializer(obj.author).data

    # def get_is_following(self, obj):
    #     return UserSerializer(obj.author).data

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'main_image', 'price', 'created', 'author')
        # fields = ('id', 'url', 'title', 'main_image', 'price', 'created', 'author')


# class ImagesAssociatedAdvertisementSerializer(ModelSerializer):
#     class Meta:
#         model = AdvertisementImage
#         fields = ('id',  'is_active', 'image')
#
#     # def get_image_url(self, obj):
#     #     return obj.image.url
#
#
# class AdvertisementSerializer(ModelSerializer):
# # class AdvertisementSerializer(HyperlinkedModelSerializer):
#
#     author = SerializerMethodField('get_author_details')
#
#     def get_author_details(self, obj):
#         return UserSerializer(obj.author).data
#
#     class Meta:
#         model = Advertisement
#         fields = ('id', 'title', 'main_image', 'price', 'created', 'author')


class ImagesAssociatedAdvertisementSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = AdvertisementImage
        fields = ('id',  'is_active', 'image')


# class AdvertisementSerializer(HyperlinkedModelSerializer):
class AdvertisementSerializer(ModelSerializer):
    # author = SerializerMethodField(source='author.username')
    images = ImagesAssociatedAdvertisementSerializer(many=True, read_only=True)
    # images = ImagesAssociatedAdvertisementSerializer(source='images', many=True, read_only=True)
    author = SerializerMethodField('get_author_details')

    def get_author_details(self, obj):
        # print(UserSerializer(obj.author).data)
        return UserSerializer(obj.author).data
    # print(get_author_details)
    class Meta:
        model = Advertisement
        fields = (
            'id',
            'title',
            'description',
            'main_image',
            'price',
            'created',
            'author',
            'category_equipment',
            'location_author',
            'images'
        )


# class AdvertisementSerializer(HyperlinkedModelSerializer):
class AdvertisementCreateUpdateSerializer(ModelSerializer):
    images = ImagesAssociatedAdvertisementSerializer(many=True, read_only=True)
    author = SerializerMethodField('get_author_details')

    def get_author_details(self, obj):
        return UserSerializer(obj.author).data

    class Meta:
        model = Advertisement
        fields = (
            'id',
            'title',
            'description',
            'main_image',
            'price',
            'created',
            'author',
            'phone_author',
            'category_equipment',
            'location_author',
            'images'
        )

    def create(self, validated_data):
        images_data = self.context.get('view').request.FILES
        advertisement = Advertisement.objects.create(**validated_data)
        for image_data in images_data.values():
            AdvertisementImage.objects.create(advertisement=advertisement, image=image_data)
        return advertisement

    def update(self, instance, validated_data):
        request = self.context.get('request')
        # images = validated_data.get('images')
        images = request.data.get('image_1', []) if request else []
        # images_data = self.context.get('view').request.FILES
        print('картинки -', images)
        print('instance - is', instance)
        for img in images:
            data = {'image': img, 'advertisement': instance}
            print('картинкa -', data)
            imageserializer = ImagesAssociatedAdvertisementSerializer(data)
            print('картинкa serialisation-', imageserializer.data)
            if imageserializer.is_valid():
                imageserializer.save()
        # return instance
        return super(AdvertisementCreateUpdateSerializer, self).update(instance, validated_data)

                # def create(self, validated_data):
    #     images_data = self.context.get('view').request.FILES
    #     # images_data = validated_data.get.pop('images')
    #     advertisement = Advertisement.objects.create(**validated_data)
    #     # author = self.author
    #     # advertisement = Advertisement.objects.create(validated_data)
    #     for image_data in images_data.values():
    #         Advertisement.objects.create(advertisement=advertisement, **image_data)
    #     print(advertisement)
    #     return advertisement
    #     # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SingleAdsSerializer(ModelSerializer):
    images = ImagesAssociatedAdvertisementSerializer(many=True, read_only=True)

    class Meta:
        model = Advertisement
        fields = (
            'title',
            'description',
            'phone_author',
            'category_equipment',
            'location_author',
            'main_image',
            'price',
            # 'author',
            'images'
        )

    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.phone_author = validated_data.get('phone_author', instance.phone_author)
    #     instance.category_equipment = validated_data.get('category_equipment', instance.category_equipment)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.main_image = validated_data.get('main_image', instance.main_image)
    #     # instance.price = validated_data.get('price', instance.price)
    #     # instance.author_id = validated_data.get('author_id', instance.author_id)
    #     instance.location_author = validated_data.get('location_author', instance.location_author)
    #     instance.save()
    #     return instance


# class AdvertisementCreateSerializer(ModelSerializer):
class AdvertisementCreateSerializer(HyperlinkedModelSerializer):

    author = SerializerMethodField('get_author_details')
    images = ImagesAssociatedAdvertisementSerializer(many=True)

    def get_author_details(self, obj):
        return UserSerializer(obj.author).data

    class Meta:
        model = Advertisement
        fields = (
            'id',
            'title',
            'main_image',
            'phone_author',
            'price',
            'description',
            'product_number',
            'location_author',
            # 'created',
            # 'updated',
            'author',
            'images',
            # 'is_moderated',
            # 'is_visible'
        )

    def create(self, validated_data):
        images_data = self.context.get('images').request.FILES

        advertisement = self.model.objects.create(title=validated_data.get('title', 'no-title'),
                                                  user_id=1)
        # advertisement = self.model.objects.create(title=validated_data.get('title', 'no-title'),
        #                                           user_id=1)
        for image_data in images_data.values():
            AdvertisementImage.objects.create(advertisement=advertisement, image=image_data)
        return advertisement


class FavoriteAdvertisementSerializer(ModelSerializer):
    advertisement = SerializerMethodField('get_ads_details')
    follower = SerializerMethodField('get_follower_details')

    def get_ads_details(self, obj):
        return AdsListSerializer(obj.advertisement).data

    def get_follower_details(self, obj):
        follower = obj.user
        return UserSerializer(follower).data

    class Meta:
        model = AdvertisementFollowing
        fields = (
            'id',
            'follower',
            'advertisement'
        )
