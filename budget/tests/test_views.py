from django.test import TestCase,Client
from django.urls import reverse,resolve
from budget.models import Category,Expense,Project
import json

class TestViews(TestCase):
     
    def setUp(self):
        self.client = Client() 
        self.list_url = reverse('list')
        self.starfeeds = Project.objects.create(name="starfeeds",budget=200000)
        self.detail_url = reverse('detail',args=['starfeeds'])

    def test_project_list_GET(self):
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'budget/project-list.html')

    def test_project_detail_GET(self):
        response = self.client.get(self.detail_url)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'budget/project-detail.html')
    
    def test_project_detail_POST_add_new_expense(self):
        Category.objects.create(project=self.starfeeds,name = 'Design')

        response = self.client.post(self.detail_url,{
             "title":"expense1",
             "amount":2000,
             "category":"Design"
        })
        self.assertEquals(response.status_code,302)
        self.assertEquals(Expense.objects.filter(project=self.starfeeds).first().project.name,'starfeeds')
        self.assertEquals(self.starfeeds.expenses.first().title,'expense1')

    def test_project_detail_POST_no_data(self):
        response = self.client.post(self.detail_url)
        self.assertEquals(response.status_code,302)
        self.assertEquals(self.starfeeds.expenses.count(),0)

    def test_project_detail_DELETE_delete_expense(self):
        category1 = Category.objects.create(project=self.starfeeds,name = 'Design')
        Expense.objects.create(
            title = "expense1",
            project = self.starfeeds,
            amount = 2000,
            category = category1
        )
        response = self.client.delete(self.detail_url,json.dumps({"id":1}))
        self.assertEquals(response.status_code,204)
        self.assertEquals(self.starfeeds.expenses.count(),0)

    def test_project_detail_DELETE_delete_no_id(self):
        category1 = Category.objects.create(project=self.starfeeds,name = 'Design')
        Expense.objects.create(
            title = "expense1",
            project = self.starfeeds,
            amount = 2000,
            category = category1
        )
        response = self.client.delete(self.detail_url)
        self.assertEquals(response.status_code,404)
        self.assertEquals(self.starfeeds.expenses.count(),1)

    def test_project_create_POST(self):
        url = reverse('add')
        response = self.client.post(url,{
            "name":"project2",
            "budget":50000,
            "categoriesString":"Design,Development"
        })
        self.assertEquals(response.status_code,302)
        project2 = Project.objects.get(id=2)
        self.assertEquals(project2.name,'project2')
        self.assertEquals(project2.category_set.count(),2)
        category1 = Category.objects.get(id=1)
        self.assertEquals(category1.name,'Design')
        category2 = Category.objects.get(id=2)
        self.assertEquals(category2.name,'Development')
       