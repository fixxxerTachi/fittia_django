#coding: utf-8
from django.shortcuts import render,redirect
from django import forms
from payment.models import UserProfile,Select
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from products.models import *
from django import forms
def login_select(request):
	form=LoginForm()
	return render(request,'payment/login_select.html',dict(form=form))

class LoginForm(forms.Form):
	email=forms.EmailField(max_length=255,label=u'メールアドレス')
	password=forms.CharField(max_length=10,label=u'パスワード',widget=forms.PasswordInput)

class AddressForm(forms.Form):
	name=forms.CharField(max_length=100)
	furigana=forms.CharField(max_length=100)
	zip_first=forms.CharField(max_length=3)
	zip_last=forms.CharField(max_length=4)
	address=forms.CharField(max_length=255)
	email=forms.EmailField()

class LoginAddressForm(forms.Form):
	last_name=forms.CharField(max_length=20)
	first_name=forms.CharField(max_length=20)
	last_furigana=forms.CharField(max_length=100)
	first_furigana=forms.CharField(max_length=100)
	zip_first=forms.CharField(max_length=3)
	zip_last=forms.CharField(max_length=4)
	prefecture=forms.CharField(max_length=10)
	city=forms.CharField(max_length=100)
	address=forms.CharField(max_length=255)

class CartAddress():
	pass

def address_form(request):
	if request.method=='POST':
		form=AddressForm(request.POST)
		if request.user.is_authenticated():
			form=LoginAddressForm(request.POST)
		if form.is_valid():
			data=form.cleaned_data
			if request.user.is_authenticated():
				uf=UserProfile()
				uf.user=request.user
				uf.first_furigana=data.get('first_furigana')
				uf.last_furigana=data.get('last_furigana')
				uf.zip_code_first=data.get('zip_first')
				uf.zip_code_last=data.get('zip_last')
				uf.prefecture=data.get('prefecture')
				uf.city=data.get('city')
				uf.address=data.get('address')
				uf.save()
			else:
				request.session['address']=form.cleaned_data
			return redirect('/payment/no_user/')

	else:
		form=AddressForm()
		if request.user.is_authenticated():
			form=LoginAddressForm()
	return render(request,'payment/address_form.html',dict(form=form))

def payment(request,flag):
	cart=request.session.get('cart',None)
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
				if lens_data['get_lens_data']=='1':
					lens_data_input=True
			else:
				lens=NoLens.objects.get(pk=int(lens_data['no_lens']))
		products[k]=product

	lens_data=request.session.get('lens_data',None)
	address=request.session.get('address',None)
	payment=request.session.get('payment',None)

	s_user=None
	user=None
	if request.user.is_authenticated():
		s_user=request.user
		user_p=UserProfile.objects.get(user=request.user)
		'''
		if flag in u'user':
			try:
				user=request.user
				user_p=UserProfile.objects.get(user=user.id)
			except:
				user_p=None
				return redirect('/no_user/')
		'''
	return render(request,'payment/show_cart.html',
		dict(cart=cart,lens_data=lens_data,address=address,products=products,lens_level=lens_level,flag=flag,payment=payment,
			user=s_user,lens_data_input=lens_data_input,	
		))
	
class PaymentSelect(forms.Form):
	payment=forms.ModelChoiceField(queryset=Select.objects.all(),empty_label=None,label='',widget=forms.RadioSelect)

def payment_select(request,flag):
	if request.method=='POST':
		form=PaymentSelect(request.POST)
		if form.is_valid():
			request.session['payment']=form.cleaned_data['payment']
			return redirect('/payment/' + flag + '/')
	else:
		form=PaymentSelect()
	return render(request,'payment/payment_select.html',dict(form=form))

def input_user(request):
	if request.method=='POST':
		form=LoginForm(request.POST)
		if form.is_valid():
			data=form.cleaned_data
			user=User.objects.create_user(
				username=data.get('email'),password=data.get('password')
			)
			user.save()
			return redirect('/login_form/')
	form=LoginForm()
	message=u'メールアドレスとパスワードを入力してください'
	return render(request,'payment/input_user.html',dict(form=form,message=message))

def login_form(request):
	message=''
	if request.method=='POST':
		form=LoginForm(request.POST)
		if form.is_valid():
			data=form.cleaned_data
			user=authenticate(username=data.get('email'),password=data.get('password'))
			if user is not None:
				if user.is_active:
					login(request,user)
					user_address=UserProfile.objects.get(user=request.user)
					if user_address:
						return redirect('/payment/user/')
					else:
						return redirect('/no_user/')
			else:
				message=u'ログインできません'
	else:
		form=LoginForm()
	return render(request,'payment/login_form.html',dict(form=form,message=message))

def logout_action(request):
	logout(request)
	return redirect('/show_cart/') 
	'''
	if request.method=='POST':
		form=LoginForm(request.POST)
		if form.is_valid():
			data=form.cleaned_data
			if flag not in u'create':
				user=authenticate(username=data.get('email'),password=data.get('password'))
				if user.is_active:
					login(request,user)
					return redirect('/payment/user/')
				else:
					return render(request,'payment_input.user.html',dict(form=LoginForm()))
			elif flag in u'create':
				user=User.objects.create_user(
					username=data.get('email'),password=data.get('password')
				)
				user.save()
				message=u'ログインしてください'
				flag='login'
				return render(request,'payment/input_user.html',dict(form=LoginForm(),message=message,flag=flag))
	else:
		form=LoginForm()
		message=u'メールアドレスとパスワードを入力してください'
		flag='create'
		return render(request,'payment/input_user.html',dict(form=form,message=message,flag=flag))
	'''
