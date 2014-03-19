#coding: utf-8
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from order.models import *
from django.shortcuts import redirect,render
def order(request):
	address=request.session.get('address',None)
	payment=request.session.get('payment',None)
	lens_level=request.session.get('lens_level',None)
	cart=request.session.get('cart',None)
	nouser=NoUser.objects.create(
		name=address['name'],
		zip_first=address['zip_first'],
		zip_last=address['zip_last'],
		address=address['address'],
		email=address['email'],
		level_l=lens_level['level_l'],
		level_r=lens_level['level_r'],
		astig_l=lens_level['astig_l'],
		astig_r=lens_level['astig_r'],
	)
	if request.user.is_authenticated():
		order=Orders.objects.create(
			payment=payment,
			customer_id=None,
			user=request.user
		)
	else:
		order=Orders.objects.create(
			payment=payment,
			customer=nouser,
			user_id=None
		)
	cart=request.session.get('cart',None)
	for c in cart:
		if c.lens_data['select_lens']=='leveled':
			oi=OrdersInfo(
				product_id=c.product_id,
				orders=order,
				lens_type=c.lens_data['select_lens'],
				leveled_lens_id=int(c.lens_data['leveled_lens']),
			)
		else:
			oi=OrdersInfo(
				product_id=c.product_id,
				orders=order,
				lens_type=c.lens_data['select_lens'],
				no_lens_id=int(c.lens_data['no_lens']),
			)
		oi.save()
	return redirect('/thanks/')	

def thanks(request):
	del(request.session['cart'])
	return render(request,'thanks.html')
