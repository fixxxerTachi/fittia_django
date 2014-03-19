#coding: utf-8 
from django.shortcuts import render,get_object_or_404,redirect
from products.models import *
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django import forms
from django.views.decorators.cache import cache_page
@cache_page(60*15)
def catalogue(request):
	products=Products.objects.select_related().all().order_by('-created')
	if request.method=='GET':
		form=SearchForm(request.GET)
		if form.is_valid():
			data=form.cleaned_data
			if data.get('order')=='p':
				products=products.order_by('price')
			if data.get('type'):
				products=products.filter(type__in=data.get('type'))
			if data.get('target'):
				products=products.filter(brand__target__in=data.get('target'))
			if data.get('sex'):	
				products=products.filter(brand__sex__in=data.get('sex'))
			if data.get('color'):
				products=products.filter(color__in=data.get('color'))

	paginator=Paginator(products,9)
	page=request.GET.get('page')
	try: 
		products=paginator.page(page)
	except PageNotAnInteger:
		products=paginator.page(1)
	except EmptyPage:
		products=paginator.page(paginator.num_pages)

	import re
	query=re.sub(r'page=\d&','',request.META['QUERY_STRING'])
	return render(request,'catalogue.html',dict(products=products,form=form,query=query))

class SearchForm(forms.Form):
	ORDER_LIST=(('n',u'新着順'),('p',u'価格の安い順'))
	order=forms.ChoiceField(choices=ORDER_LIST,required=False)
	type=forms.ModelMultipleChoiceField(Type.objects.all(),label=u'形',required=False,widget=forms.CheckboxSelectMultiple)
	target=forms.ModelMultipleChoiceField(Target.objects.all(),required=False,widget=forms.CheckboxSelectMultiple)
	sex=forms.ModelMultipleChoiceField(Sex.objects.all(),required=False,widget=forms.CheckboxSelectMultiple)
	color=forms.ModelMultipleChoiceField(Color.objects.all(),required=False,widget=forms.CheckboxSelectMultiple)

def view(request,product_id):
	product=get_object_or_404(Products,id=product_id)
	return render(request,'view.html',dict(product=product))

'''
def insert_cart(request,product_id):
	cart=request.session.get('cart',None)
	if not cart:
		cart=[product_id]
	else:
		cart.append(product_id)
	request.session['cart']=cart
	return redirect('/show_cart/')

def show_cart(request):
	cart=request.session.get('cart',[])
	products=Products.objects.filter(id__in=cart)	
	return render(request,'show_cart.html',dict(cart=cart,products=products))
'''

class Cart(object):
	lens_data=False
class Personals(object):
	pass

def insert_cart(request,product_id):
	cart=request.session.get('cart',[])
	c=Cart()
	c.product_id=product_id
	cart.append(c)
	request.session['cart']=cart
	return redirect('/show_cart/')

def show_cart(request):
	cart=request.session.get('cart',[])
	products={}
	lens=''
	lens_data_input=False
	lens_level=request.session.get('lens_level',None)
	for k,c in enumerate(cart):
		product=Products.objects.get(pk=c.product_id)
		if cart[int(k)].lens_data:
			product.checked=True
			product.cart=cart[int(k)]
			lens_data=cart[int(k)].lens_data
			if lens_data['select_lens']=='leveled':
				lens=LeveledLens.objects.get(pk=int(lens_data['leveled_lens']))
				if lens_data['get_lens_data'] == '1':
					lens_data_input=True
			else:
				lens=NoLens.objects.get(pk=int(lens_data['no_lens']))
				
		products[k]=product
		'''
		products.append(product)
		'''
	return render(request,'show_cart.html',dict(
		cart=cart,products=products,lens=lens,lens_data_input=lens_data_input,lens_level=lens_level))

def empty_cart(request):
	del(request.session['cart'])
	personals=request.session.get('lens_data',None)
	if personals:
		del(request.session['lens_data'])
	return redirect('/')

def del_item(request,cart_counter):
	del(request.session['cart'][int(cart_counter)])
	request.session.modified=True
	return redirect('/show_cart/')

class LensForm(forms.Form):
	CHOICES=(('leveled',u'度つきレンズを選択'),('no_lens','度なしレンズを選択'))
	select_lens=forms.ChoiceField(choices=CHOICES,label=u'度つきか度なしレンズを選択できます')
	no_lens=forms.ModelChoiceField(NoLens.objects.all(),required=False,label=u'度なしレンズの種類')
	leveled_lens=forms.ModelChoiceField(LeveledLens.objects.all(),required=False,label=u'度つきレンズの種類')
	enkin_lens=forms.ModelChoiceField(EnkinLens.objects.all(),required=False,label=u'レンズの種類(近視用、遠視用)')
	get_lens_data=forms.ModelChoiceField(GetLensData.objects.all(),required=False,label=u'レンズデータの取得方法')
	def clean(self):
		cleaned_data=self.cleaned_data
		'''
		if cleaned_data['no_lens'] is None and cleaned_data['leveled_lens'] is None:
			raise forms.ValidationError(u'項目を選択してください')
		'''
		if cleaned_data['select_lens']=='leveled':
			if cleaned_data['leveled_lens'] is None or cleaned_data['enkin_lens'] is None or cleaned_data['get_lens_data'] is None:
				raise forms.ValidationError(u'項目を選択してください')

		return cleaned_data
		
def select_lens(request,cart_counter,checked=None,flag=None):
	if request.method=='POST':
		form=LensForm(request.POST)
		c=Cart()
		if form.is_valid():
			c.product_id=request.session['cart'][int(cart_counter)].product_id
			'''
			c.lens_data=form.cleaned_data
			'''
			c.lens_data=request.POST
			request.session['cart'][int(cart_counter)]=c
			request.session.modified=True
			if flag=='payment':
				return redirect('/payment/no_user/')
			else:
				return redirect('/show_cart/')

	elif checked=='checked':
		data=request.session['cart'][int(cart_counter)].lens_data
		data=dict(
			select_lens=data['select_lens'],
			no_lens=data['no_lens'],
			leveled_lens=data['leveled_lens'],
			enkin_lens=data['enkin_lens'],
			get_lens_data=data['get_lens_data'],
		)
		form=LensForm(data)
	else:
		form=LensForm()
		data=''
	return render(request,'select_lens.html',dict(form=form,data=data))

class LensDataInput(object):
	def generate_level(self):
		x=-16.00
		while True:
			yield x
			x += 0.25
	
	def get_level_data(self):
		data=self.generate_level()
		return [next(data) for i in range(105)]

	def generate_astig(self):
		x=-4.00
		while True:
			yield x
			x += 0.25

	def get_astig_data(self):
		data=self.generate_astig()
		return [next(data) for i in range(33)]
	
class LensDataForm(forms.Form):
	LevelChoices=(
		(0,-10.00),(1,-9.50),(2,-8.00),(3,-7.50),(4,0.00),
	)
	level_r=forms.ChoiceField(choices=LevelChoices,initial=4)
	level_l=forms.ChoiceField(choices=LevelChoices,initial=4)
	astig_r=forms.ChoiceField(choices=LevelChoices,initial=4)
	astig_l=forms.ChoiceField(choices=LevelChoices,initial=4)
	
def lens_data_input(request,flag=None):
	if request.method=='POST':
		form=LensDataForm(request.POST)
		if form.is_valid():
			'''
			data=Personals()
			data.input_data=form.cleaned_data
			request.session['lens_data']=data
			'''
			request.session['lens_level']=form.cleaned_data
			if flag=='payment':
				return redirect('/payment/no_user/')
			else:
				return redirect('/show_cart/')
	
	personals=request.session.get('lens_data',None)
	if personals:
		input_data=personals.input_data or None
	else:
		input_data=None
	form=LensDataForm(input_data)
	return render(request,'lens_data_input.html',dict(form=form))
