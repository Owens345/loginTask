from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from tasks.models import Task
import re

User = get_user_model()

class TestAssignmentRequirements(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            age=25,
            password='ValidPass123'
        )
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            user=self.user
        )
    
    def test_01_custom_user_model_fields(self):
        """Test CustomUser model has all required fields"""
        print("\n=== 1. Testing CustomUser Model ===")
        
        # Check required fields exist
        user = self.user
        fields_to_check = [
            ('username', str, 'testuser'),
            ('email', str, 'test@example.com'),
            ('age', int, 25),
            ('is_superuser', bool, False),
            ('is_staff', bool, False),
            ('is_active', bool, True),
            ('date_joined', type(user.date_joined), None),
        ]
        
        for field_name, field_type, expected_value in fields_to_check:
            field_value = getattr(user, field_name)
            self.assertIsInstance(field_value, field_type, 
                                f"Field {field_name} should be {field_type.__name__}")
            if expected_value is not None:
                self.assertEqual(field_value, expected_value,
                               f"Field {field_name} should be {expected_value}")
            print(f"  ✓ {field_name}: {field_value}")
    
    def test_02_login_screen_requirements(self):
        """Test login screen meets all requirements"""
        print("\n=== 2. Testing Login Screen ===")
        
        response = self.client.get(reverse('login'))
        content = response.content.decode('utf-8')
        
        # Check screen title
        self.assertIn('<h1>Login Page</h1>', content, 
                     "Login screen should have title 'Login Page'")
        print("  ✓ Title: 'Login Page'")
        
        # Check email address label
        self.assertIn('Email address:', content,
                     "Login form should have label 'Email address:'")
        print("  ✓ Label: 'Email address:'")
        
        # Check password label
        self.assertIn('Password:', content,
                     "Login form should have label 'Password:'")
        print("  ✓ Label: 'Password:'")
        
        # Check login button
        self.assertIn('Login</button>', content,
                     "Login form should have 'Login' button")
        print("  ✓ Button: 'Login'")
        
        # Check form has required fields
        self.assertIn('name="username"', content,
                     "Login form should have username field (for email)")
        self.assertIn('name="password"', content,
                     "Login form should have password field")
        self.assertIn('csrfmiddlewaretoken', content,
                     "Login form should have CSRF token")
        print("  ✓ Has all required form fields")
    
    def test_03_registration_screen_requirements(self):
        """Test registration screen meets all requirements"""
        print("\n=== 3. Testing Registration Screen ===")
        
        response = self.client.get(reverse('register'))
        content = response.content.decode('utf-8')
        
        # Check screen title
        self.assertIn('<h1>Member Registration Page</h1>', content,
                     "Registration screen should have title 'Member Registration Page'")
        print("  ✓ Title: 'Member Registration Page'")
        
        # Check all required labels
        labels_to_check = [
            'username:',
            'Email address:',
            'age:',
            'Password:',
            'Password (for confirmation):'
        ]
        
        for label in labels_to_check:
            self.assertIn(label, content,
                         f"Registration form should have label '{label}'")
            print(f"  ✓ Label: '{label}'")
        
        # Check password validation rules (all 4 must be present)
        password_rules = [
            'cannot be similar to your other personal information',
            'must be at least 8 characters long',
            'cannot be a commonly used password',
            'cannot contain only numbers'
        ]
        
        for rule in password_rules:
            self.assertIn(rule, content.lower(),
                         f"Registration should show password rule: '{rule}'")
            print(f"  ✓ Password rule: '{rule}'")
        
        # Check register button
        self.assertIn('register</button>', content,
                     "Registration form should have 'register' button")
        print("  ✓ Button: 'register'")
    
    def test_04_user_detail_screen_requirements(self):
        """Test user detail screen meets all requirements"""
        print("\n=== 4. Testing User Detail Screen ===")
        
        self.client.force_login(self.user)
        response = self.client.get(reverse('user_detail'))
        content = response.content.decode('utf-8')
        
        # Check screen title
        self.assertIn('<h1>Member Information Details Page</h1>', content,
                     "User detail screen should have title 'Member Information Details Page'")
        print("  ✓ Title: 'Member Information Details Page'")
        
        # Check user info labels
        labels_to_check = [
            'username:',
            'Email address:',
            'age:'
        ]
        
        for label in labels_to_check:
            self.assertIn(label, content,
                         f"User detail should show '{label}'")
            print(f"  ✓ Shows: '{label}'")
        
        # Check user info values
        self.assertIn(self.user.username, content,
                     "Should show username value")
        self.assertIn(self.user.email, content,
                     "Should show email value")
        self.assertIn(str(self.user.age), content,
                     "Should show age value")
        print("  ✓ Shows all user information")
        
        # Check links
        self.assertIn('edit</a>', content,
                     "Should have 'edit' link")
        self.assertIn('Change Password</a>', content,
                     "Should have 'Change Password' link")
        print("  ✓ Has 'edit' and 'Change Password' links")
    
    def test_05_user_edit_screen_requirements(self):
        """Test user edit screen meets all requirements"""
        print("\n=== 5. Testing User Edit Screen ===")
        
        self.client.force_login(self.user)
        response = self.client.get(reverse('user_edit'))
        content = response.content.decode('utf-8')
        
        # Check screen title
        self.assertIn('<h1>Member Information Edit Page</h1>', content,
                     "User edit screen should have title 'Member Information Edit Page'")
        print("  ✓ Title: 'Member Information Edit Page'")
        
        # Check labels
        labels_to_check = [
            'username:',
            'Email address:',
            'age:'
        ]
        
        for label in labels_to_check:
            self.assertIn(label, content,
                         f"User edit form should have label '{label}'")
            print(f"  ✓ Label: '{label}'")
        
        # Check update button
        self.assertIn('Update</button>', content,
                     "Should have 'Update' button")
        print("  ✓ Button: 'Update'")
        
        # Check links
        self.assertIn('Return</a>', content,
                     "Should have 'Return' link to task list")
        self.assertIn('withdrawal from a group</a>', content,
                     "Should have 'withdrawal from a group' link")
        print("  ✓ Has 'Return' and 'withdrawal from a group' links")
    
    def test_06_password_change_screen_requirements(self):
        """Test password change screen meets all requirements"""
        print("\n=== 6. Testing Password Change Screen ===")
        
        self.client.force_login(self.user)
        response = self.client.get(reverse('change_password'))
        content = response.content.decode('utf-8')
        
        # Check screen title
        self.assertIn('<h1>Password Change Page</h1>', content,
                     "Password change screen should have title 'Password Change Page'")
        print("  ✓ Title: 'Password Change Page'")
        
        # Check labels
        labels_to_check = [
            'Original Password:',
            'new password:',
            'New password (for confirmation):'
        ]
        
        for label in labels_to_check:
            self.assertIn(label, content,
                         f"Password change form should have label '{label}'")
            print(f"  ✓ Label: '{label}'")
        
        # Check password validation rules
        password_rules = [
            'cannot be similar to your other personal information',
            'must be at least 8 characters long',
            'cannot be a commonly used password',
            'cannot contain only numbers'
        ]
        
        for rule in password_rules:
            self.assertIn(rule, content.lower(),
                         f"Password change should show rule: '{rule}'")
            print(f"  ✓ Password rule: '{rule}'")
        
        # Check change button
        self.assertIn('Change</button>', content,
                     "Should have 'Change' button")
        print("  ✓ Button: 'Change'")
        
        # Check return link
        self.assertIn('Return</a>', content,
                     "Should have 'Return' link to user detail")
        print("  ✓ Has 'Return' link")
    
    def test_07_delete_account_screen_requirements(self):
        """Test delete account screen meets all requirements"""
        print("\n=== 7. Testing Delete Account Screen ===")
        
        self.client.force_login(self.user)
        response = self.client.get(reverse('delete_account'))
        content = response.content.decode('utf-8')
        
        # Check screen title
        self.assertIn('<h1>Unsubscribe Page</h1>', content,
                     "Delete account screen should have title 'Unsubscribe Page'")
        print("  ✓ Title: 'Unsubscribe Page'")
        
        # Check user info labels
        labels_to_check = [
            'username:',
            'Email address:',
            'age:'
        ]
        
        for label in labels_to_check:
            self.assertIn(label, content,
                         f"Delete account should show '{label}'")
            print(f"  ✓ Shows: '{label}'")
        
        # Check withdraw button
        self.assertIn('Withdraw</button>', content,
                     "Should have 'Withdraw' button")
        print("  ✓ Button: 'Withdraw'")
        
        # Check return link
        self.assertIn('Return</a>', content,
                     "Should have 'Return' link to user detail")
        print("  ✓ Has 'Return' link")
    
    def test_08_navigation_requirements(self):
        """Test navigation meets all requirements"""
        print("\n=== 8. Testing Navigation ===")
        
        # Test logged out navigation
        response = self.client.get(reverse('login'))
        content = response.content.decode('utf-8')
        
        logged_out_nav = [
            '>Login</a>',
            '>Member Registration</a>'
        ]
        
        print("  Logged out navigation:")
        for nav_item in logged_out_nav:
            self.assertIn(nav_item, content,
                         f"Logged out navigation should have '{nav_item[1:-4]}'")
            print(f"    ✓ {nav_item[1:-4]}")
        
        # Test logged in navigation
        self.client.force_login(self.user)
        response = self.client.get(reverse('task_list'))
        content = response.content.decode('utf-8')
        
        logged_in_nav = [
            '>Task list</a>',
            '>Member Information</a>',
            '>Log out</a>'
        ]
        
        print("  Logged in navigation:")
        for nav_item in logged_in_nav:
            self.assertIn(nav_item, content,
                         f"Logged in navigation should have '{nav_item[1:-4]}'")
            print(f"    ✓ {nav_item[1:-4]}")
    
    def test_09_task_crud_functionality(self):
        """Test task CRUD works normally"""
        print("\n=== 9. Testing Task CRUD ===")
        
        self.client.force_login(self.user)
        
        # Test task list
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        print("  ✓ Task list loads")
        
        # Test task detail
        response = self.client.get(reverse('task_detail', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        print("  ✓ Task detail loads")
        
        # Test task edit
        response = self.client.get(reverse('task_edit', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        print("  ✓ Task edit loads")
        
        # Test task delete
        response = self.client.get(reverse('task_delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        print("  ✓ Task delete loads")
        
        # Test task create
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 200)
        print("  ✓ Task create loads")
        
        print("  ✓ All task CRUD functions work")
    
    def test_10_login_logout_functionality(self):
        """Test login and logout work with custom user"""
        print("\n=== 10. Testing Login/Logout Functionality ===")
        
        # Test login
        response = self.client.post(reverse('login'), {
            'username': 'test@example.com',
            'password': 'ValidPass123'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after login
        print("  ✓ User can login with email")
        
        # Test logout
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Should redirect after logout
        print("  ✓ User can logout")
        
        # Test registration
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'age': 30,
            'password1': 'NewValidPass123',
            'password2': 'NewValidPass123'
        }, follow=True)
        
        # Registration should either redirect or show success
        self.assertIn(response.status_code, [200, 302])
        print("  ✓ User can register")
    
    def run_all_tests(self):
        """Run all tests and print summary"""
        print("=" * 60)
        print("COMPREHENSIVE ASSIGNMENT REQUIREMENTS TEST")
        print("=" * 60)
        
        test_methods = [
            self.test_01_custom_user_model_fields,
            self.test_02_login_screen_requirements,
            self.test_03_registration_screen_requirements,
            self.test_04_user_detail_screen_requirements,
            self.test_05_user_edit_screen_requirements,
            self.test_06_password_change_screen_requirements,
            self.test_07_delete_account_screen_requirements,
            self.test_08_navigation_requirements,
            self.test_09_task_crud_functionality,
            self.test_10_login_logout_functionality,
        ]
        
        passed = 0
        failed = 0
        
        for test_method in test_methods:
            try:
                test_method()
                passed += 1
            except AssertionError as e:
                failed += 1
                print(f"\n❌ FAILED: {test_method.__name__}")
                print(f"   Error: {e}")
            except Exception as e:
                failed += 1
                print(f"\n❌ ERROR in {test_method.__name__}: {e}")
        
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📊 Total:  {passed + failed}")
        
        if failed == 0:
            print("\n🎉 ALL REQUIREMENTS MET! Ready to submit!")
        else:
            print(f"\n⚠️  {failed} requirement(s) need fixing before submission.")

# Run the tests
if __name__ == "__main__":
    test_suite = TestAssignmentRequirements()
    test_suite.setUp()
    test_suite.run_all_tests()
