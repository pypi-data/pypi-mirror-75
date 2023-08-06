from typing import Dict, List

from remo_app.remo.models import AnnotationSet, Tag, Annotation, AnnotationTags, DatasetImage
from remo_app.remo.stores.image_store import ImageStore
from remo_app.remo.use_cases.annotation import update_new_annotation
from remo_app.remo.use_cases.jobs.update_annotation_set_statistics import count_tags, \
    get_or_create_annotation_set_statistics


class TagStore:

    @staticmethod
    def get_tag(name: str) -> Tag:
        name = name.strip().lower()
        if name:
            tag, _ = Tag.objects.get_or_create(name=name)
            return tag

    @staticmethod
    def _get_or_create_annotation(image, annotation_set):
        annotation = Annotation.objects.filter(image=image, annotation_set=annotation_set).first()
        if not annotation:
            annotation = Annotation.objects.create(
                image=image,
                annotation_set=annotation_set
            )
        return annotation

    @staticmethod
    def update_annotation_set_tags_statistics(annotation_set: AnnotationSet, annotation: Annotation):
        stat = get_or_create_annotation_set_statistics(annotation_set)
        stat.tags = count_tags(annotation_set.id)
        stat.save()

        update_new_annotation(annotation)

    @staticmethod
    def add_tag_to_image(image: DatasetImage, annotation_set: AnnotationSet, name: str):
        tag = TagStore.get_tag(name)
        if not tag:
            return
        annotation = TagStore._get_or_create_annotation(image, annotation_set)
        annotation_tag = AnnotationTags.objects.filter(tag=tag, image=image, annotation=annotation,
                                                       annotation_set=annotation_set).first()
        if annotation_tag:
            return

        annotation_tag = AnnotationTags(tag=tag, image=image, annotation=annotation, annotation_set=annotation_set)
        annotation_tag.save()

    @staticmethod
    def add_tags_to_annotation_set(image_tags: Dict[str, List[str]], annotation_set_id: int) -> List[str]:
        missing_images = set()
        annotation_set = AnnotationSet.objects.get(id=annotation_set_id)
        for img_name, tags in image_tags.items():
            img = ImageStore.get_image(annotation_set.dataset.id, img_name)
            if not img:
                missing_images.add(img_name)
                continue
            for tag in tags:
                TagStore.add_tag_to_image(img, annotation_set, tag)
            annotation = TagStore._get_or_create_annotation(img, annotation_set)
            TagStore.update_annotation_set_tags_statistics(annotation_set, annotation)
        return list(missing_images)
