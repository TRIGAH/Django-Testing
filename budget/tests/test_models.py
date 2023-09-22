from django.test import TestCase
from budget.models import Project,Category,Expense

class TestModels(TestCase):

    def setUp(self):
        self.project3 = Project.objects.create(
            name = 'project 3',
            budget = 50000
        )

    def test_project_create_slug_ON_SAVE(self):
        self.assertEquals(self.project3.slug,"project-3")

    def test_project_budget_left_PROPERTY(self):
        category1 = Category.objects.create(
            project = self.project3,
            name = "Testing"
        )
        category2 = Category.objects.create(
            project = self.project3,
            name = "Marketing"
        )
        Expense.objects.create(
            project = self.project3,
            title = 'expense1',
            amount = 10000,
            category = category1

        )        

        self.assertEquals(self.project3.budget_left,40000)

    def test_project_total_transactions_PROPERTY(self):
        category1 = Category.objects.create(
            project = self.project3,
            name = "Testing"
        )
        category2 = Category.objects.create(
            project = self.project3,
            name = "Marketing"
        )
        Expense.objects.create(
            project = self.project3,
            title = 'expense1',
            amount = 10000,
            category = category1

        ) 
        self.assertEquals(self.project3.total_transactions,1)    