#coding: utf-8
from django.db import models
class Products(models.Model):
	code=models.CharField(u'商品コード',max_length=100)
	brand=models.ForeignKey('Brand',verbose_name=u'ブランド名')
	color=models.ForeignKey('Color',verbose_name=u'カラー')
	price=models.PositiveIntegerField(u'価格')
	type=models.ForeignKey('Type',verbose_name=u'フレームの形')
	quantity=models.PositiveIntegerField(u'在庫数')
	img=models.CharField(u'商品画像',max_length=100)
	created=models.DateTimeField(auto_now_add=True)
	modified=models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return '%s : %s ' % (self.id,self.brand)

class Color(models.Model):
	name=models.CharField(u'カラー名',max_length=100)
	code=models.CharField(u'カラーコード',max_length=100)
	def __unicode__(self):
		return self.name

class Brand(models.Model):
	name=models.CharField(u'ブランド名',max_length=100)
	code=models.CharField(u'コード名',max_length=10)
	description=models.TextField(u'説明')
	img=models.CharField(u'画像',max_length=100)
	target=models.ForeignKey('Target',verbose_name=u'ターゲット')
	sex=models.ForeignKey('Sex',verbose_name=u'性別')
	def __unicode__(self):
		return self.name

class Type(models.Model):
	name=models.CharField(u'型名',max_length=100)
	def __unicode__(self):
		return self.name

class Target(models.Model):
	name=models.CharField(u'対象',max_length=100)
	def __unicode__(self):
		return self.name

class Sex(models.Model):
	name=models.CharField(u'性別',max_length=100)
	def __unicode__(self):
		return self.name

class LeveledLens(models.Model):
	name=models.CharField(u'度つきレンズの種類',max_length=100)
	def __unicode__(self):
		return self.name

class NoLens(models.Model):
	name=models.CharField(u'度なしレンズの種類',max_length=100)
	def __unicode__(self):
		return self.name

class EnkinLens(models.Model):
	name=models.CharField(u'遠近レンズの種類',max_length=100)
	def __unicode__(self):
		return self.name

class GetLensData(models.Model):
	name=models.CharField(u'レンズデータの取得方法',max_length=255)
	def __unicode__(self):
		return self.name

