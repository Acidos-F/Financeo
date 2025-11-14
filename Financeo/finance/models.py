from django.db import models
from django.contrib.auth.models import User
from django.db import transaction as db_transaction
from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class TransactionType(models.TextChoices):
    INCOME = 'INCOME', 'Income'
    EXPENSE = 'EXPENSE', 'Expense'

class AccountType(models.TextChoices):
    CHECKING = 'CHECKING', 'Checking'
    SAVINGS = 'SAVINGS', 'Savings'
    CREDIT_CARD = 'CREDIT_CARD', 'Credit Card'
    CASH = 'CASH', 'Cash'


# --- Models based on ERD ---

class Profile(models.Model):
    """
    Represents a user's profile, with additional information like a profile picture.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Account(models.Model):
    """
    Represents a user's financial account (e.g., checking, savings).
    Tied to NFR-1.1: Belongs to one user.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="accounts"
    )
    name = models.CharField(max_length=100)
    type = models.CharField(
        max_length=50,
        choices=AccountType.choices,
        default=AccountType.CHECKING
    )
    current_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )

    def __str__(self):
        return f"{self.name} ({self.get_type_display()}) - {self.user.username}"

    class Meta:
        # A user cannot have two accounts with the same name
        unique_together = ('user', 'name')


class Category(models.Model):
    """
    A user-defined category for transactions (e.g., "Groceries", "Salary").
    Tied to NFR-1.1: Belongs to one user.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="categories"
    )
    name = models.CharField(max_length=100)
    type = models.CharField(
        max_length=10,
        choices=TransactionType.choices,
        default=TransactionType.EXPENSE
    )

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

    class Meta:
        verbose_name_plural = "Categories"
        # A user cannot have two categories with the same name and type
        unique_together = ('user', 'name', 'type')


class Transaction(models.Model):
    """
    Represents a single income or expense event.
    Implements FR-4.3: Automatically updates Account balance on save/delete.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="transactions"
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="transactions"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,  # Don't delete category if transactions use it
        related_name="transactions"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    type = models.CharField(
        max_length=10,
        choices=TransactionType.choices
    )
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.get_type_display()} - {self.amount} on {self.date}"

    def save(self, *args, **kwargs):
        """
        Custom save method to implement FR-4.3 (auto-update balance).
        Wraps the logic in an atomic transaction.
        """
        is_new = self.pk is None
        
        with db_transaction.atomic():
            if is_new:
                # This is a new transaction
                if self.type == TransactionType.INCOME:
                    self.account.current_balance += self.amount
                else:  # EXPENSE
                    self.account.current_balance -= self.amount
            else:
                # This is an update to an existing transaction
                old_self = Transaction.objects.get(pk=self.pk)
                
                # 1. Revert the old transaction from its account
                # (Handles case where account itself was changed)
                if old_self.type == TransactionType.INCOME:
                    old_self.account.current_balance -= old_self.amount
                else:
                    old_self.account.current_balance += old_self.amount
                old_self.account.save()

                # 2. Apply the new transaction to its account
                if self.type == TransactionType.INCOME:
                    self.account.current_balance += self.amount
                else:
                    self.account.current_balance -= self.amount
            
            self.account.save()
            super().save(*args, **kwargs)  # Save the transaction itself

    def delete(self, *args, **kwargs):
        """
        Custom delete method to implement FR-4.3 (auto-update balance).
        Reverts the transaction's effect on the account balance.
        """
        with db_transaction.atomic():
            if self.type == TransactionType.INCOME:
                self.account.current_balance -= self.amount
            else:  # EXPENSE
                self.account.current_balance += self.amount
            self.account.save()
            super().delete(*args, **kwargs)  # Delete the transaction itself

    class Meta:
        ordering = ['-date', '-id']


class Budget(models.Model):
    """
    A user-defined budget for a specific category over a time period.
    Tied to NFR-1.1: Belongs to one user.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="budgets"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,  # If category is deleted, budget is too
        related_name="budgets"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Budget for {self.category.name} ({self.start_date} to {self.end_date})"

    class Meta:
        # A user cannot have overlapping budgets for the same category
        unique_together = ('user', 'category', 'start_date', 'end_date')
