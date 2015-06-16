from django.views.generic import TemplateView
import json


class ReportTest(TemplateView):
	template_name = 'pathogenSite/report/test.html'

	def get_context_data(self, **kwargs): # this will call 'GET' request
		context = super(ReportTest, self).get_context_data(**kwargs)
		data = [
				['Mushrooms', 3],
				['Onions', 1], ['Olives', 1], ['Zucchini', 1], ['Pepperoni', 2]
				]
		options = {'title':'How Much Pizza I Ate Last Night', 'width':400,
				'height':300}
		total = {"cols": [\
					{"id":"","label":"Topping","pattern":"","type":"string"},\
					{"id":"","label":"Slices","pattern":"","type":"number"}],\
				"rows": [
					{"c":[{"v":"Mushrooms"},{"v":3}]},\
					{"c":[{"v":"Onions"},{"v":1}]},\
					{"c":[{"v":"Olives"},{"v":1}]},\
					{"c":[{"v":"Zucchini"},{"v":1}]},\
					{"c":[{"v":"Pepperoni"},{"v":2}]}]
				}  
		context['data']	= json.dumps(data)
		context['options']	= json.dumps(options)
		context['total'] = json.dumps(total)
		return context
