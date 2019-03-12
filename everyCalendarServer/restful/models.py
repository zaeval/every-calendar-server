from django.db import models

# Create your models here.
from rest_framework.compat import MaxValueValidator, MinValueValidator

class Friends(models.Model):
    pass
#
#
# class Tag(models.Model):
#     class Meta:
#         verbose_name_plural = "태그"
#
#     name = models.CharField(max_length=64, verbose_name="태그")
#
#     def __str__(self):
#         return self.name
#
#
# class Response(PolymorphicModel):
#     class Meta:
#         verbose_name_plural = "보기"
#
#     pass
#
#
# class Choice(models.Model):
#     class Meta:
#         verbose_name_plural = "선택지"
#
#     text = models.CharField(max_length=128, verbose_name="선택 내용", blank=True, null=True)
#
#     def __str__(self):
#         return self.text
#
#
# class Block(PolymorphicModel):
#     class Meta:
#         verbose_name_plural = "블록"
#
#     pass
#
#
# class UniqueAnswerResponse(Response):
#     class Meta:
#         verbose_name_plural = "단일선택 보기"
#
#     choices = models.ManyToManyField(Choice, verbose_name="선택지들")
#
#     answer = models.ForeignKey('Choice', verbose_name="답", on_delete=models.CASCADE, related_name='unique_answer',
#                                blank=True, null=True)
#
#
# class SequenceBlock(models.Model):
#     class Meta:
#         verbose_name_plural = "컨텍스트 블록"
#
#     blocks = models.ManyToManyField(Block, verbose_name="블록들", blank=True)
#
#
# class TextBlock(Block):
#     class Meta:
#         verbose_name_plural = "텍스트 블록"
#
#     text = models.TextField(verbose_name="텍스트")
#
#
# class TableBlock(Block):
#     class Meta:
#         verbose_name_plural = "테이블 블록"
#
#     row = models.IntegerField(verbose_name="행")
#     column = models.IntegerField(verbose_name="열")
#     blocks = models.ManyToManyField(Block, verbose_name="블록들", related_name='table_block')
#
#
# class ImageBlock(Block):
#     class Meta:
#         verbose_name_plural = "이미지 블록"
#
#     image = models.ImageField(verbose_name="이미지")
#
#
# class Question(models.Model):
#     class Meta:
#         verbose_name_plural = "문제"
#
#     name = models.CharField(max_length=64, verbose_name="문제이름")
#     response = models.ForeignKey('Response', verbose_name="보기", on_delete=models.CASCADE, blank=True, null=True)
#     context_block = models.ForeignKey('SequenceBlock', verbose_name="지문", on_delete=models.CASCADE, blank=True,
#                                       null=True)
#     tags = models.ManyToManyField(Tag, verbose_name="태그들", blank=True)
#
#
# class Exam(models.Model):
#     class Meta:
#         verbose_name_plural = "시험지"
#
#     name = models.CharField(max_length=64, verbose_name="시험지 이름")
#     questions = models.ManyToManyField(Question, verbose_name="문제들", related_name='exam_question', blank=True)
#
#     def get_questions(self):
#         return ", ".join([p.name for p in self.questions.all()])
#
#
# class Workspace(models.Model):
#     class Meta:
#         verbose_name_plural = "워크 스페이스"
#
#     title = models.CharField(max_length=64, verbose_name="제목")
#     exams = models.ManyToManyField(Exam, verbose_name="시험들", blank=True)
#     tags = models.ManyToManyField(Tag, verbose_name="태그들", blank=True)
#
#
# class Log(models.Model):
#     class Meta:
#         verbose_name_plural = "시험기록"
#
#     exam = models.ForeignKey(Exam, verbose_name="시험지", on_delete=models.CASCADE, blank=True, null=True)
#     answers = models.ManyToManyField(Choice, verbose_name="학생 답안지")
#
#
# class Student(models.Model):
#     class Meta:
#         verbose_name_plural = "학생"
#
#     name = models.CharField(max_length=64, verbose_name="이름")
#     exam_logs = models.ManyToManyField(Log, verbose_name="시험기록", blank=True)
#
#
#
# class Chapter(models.Model):
#     class Meta:
#         verbose_name_plural = "챕터(대분류)"
#     name = models.CharField(max_length=64, verbose_name="이름")
#     def __str__(self):
#         return str(self.name)
#
# class SubChapter(models.Model):
#     class Meta:
#         verbose_name_plural = "소분류"
#
#     name = models.CharField(max_length=64, verbose_name="이름")
#     chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
#     def __str__(self):
#         return str(self.name)
#
# class ProjectBlock(models.Model):
#     class Meta:
#         verbose_name_plural = "프로젝트 블록"
#
#     content = models.TextField(verbose_name="컨텐츠",null=True,blank=True)
#     subchapter = models.ForeignKey(SubChapter, on_delete=models.CASCADE)
#     style = models.TextField(verbose_name="style Json",null=True,blank=True)
#     def __str__(self):
#         return self.content[:10]+" ..."
#
# def add_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     return '{0}/resource/{1}'.format(str(instance), filename)
#
# class ProjectFile(models.Model):
#     class Meta:
#         verbose_name_plural = "파일"
#
#     project_block = models.ForeignKey(ProjectBlock, on_delete=models.CASCADE,verbose_name="프로젝트 블록")
#     file = models.FileField(verbose_name="파일",upload_to=add_directory_path)
#     project_directory = models.CharField(max_length=256,verbose_name="프로젝트 명")
#     def __str__(self):
#         return  self.project_directory
#
# class ProjectInfo(models.Model):
#     class Meta:
#         verbose_name_plural = "프로젝트 요약정보"
#
#     name = models.CharField(max_length=64, verbose_name="프로젝트 이름")
#     describe = models.CharField(max_length=256, verbose_name="프로젝트 설명")
#     difficulty = models.CharField(max_length=64, verbose_name="프로젝트 난이도")
#     tags = models.ManyToManyField(Tag, verbose_name="태그")
#     teacher = models.CharField(max_length=64, verbose_name="강사명")
#     category = models.CharField(max_length=64, verbose_name="카테고리")
#     supply = models.CharField(max_length=128, verbose_name="준비물")
#     image = models.ImageField(verbose_name="완성품 이미지",upload_to=add_directory_path)
#     thumbnail = models.ImageField(verbose_name="thumbnail 이미지",upload_to=add_directory_path,null=True,blank=True)
#     time = models.CharField(max_length=64, verbose_name="강좌 예상 소요 시간")
#     star = models.IntegerField(
#         verbose_name="평점",
#         validators=[
#             MaxValueValidator(5),
#             MinValueValidator(0)
#         ], default=0
#     )
#     student_num = models.IntegerField(verbose_name="수강생 수", default=0)
#     reviewer_num = models.IntegerField(verbose_name="리뷰 갯수", default=0)
#     def __str__(self):
#         return self.name+"_"+self.difficulty+'['+self.teacher+']'
#
# class Project(models.Model):
#     class Meta:
#         verbose_name_plural = "프로젝트"
#
#     info = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE,verbose_name="프로젝트 요약 정보")
#     chapters = models.ManyToManyField(Chapter,verbose_name="챕터(대분류)들",related_name="project_to_chapter")
#     subchapters = models.ManyToManyField(SubChapter,verbose_name="소분류들")
#     blocks = models.ManyToManyField(ProjectBlock,verbose_name="텍스트 블록들")
#     project_files = models.ManyToManyField(ProjectFile,verbose_name="리소스 들")
#
#     def __str__(self):
#         return self.info.name+"_"+self.info.difficulty+'['+self.info.teacher+']'
#
# class PreEmail(models.Model):
#     class Meta:
#         verbose_name_plural="사전 이메일 등록"
#     email = models.EmailField(verbose_name="이메일")