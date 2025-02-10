# Django Unit Testing Guide

This document provides an overview of the testing techniques used to test the Django project. The tests cover Django views and models, ensuring the correctness and reliability of the application.

## Testing Techniques Used

### 1. **Setting Up Test Data**
Before executing tests, we need to set up test data. This involves creating instances of models that can be used in multiple test cases.

**Example:** Setting up a test restaurant instance before running the tests. This ensures that we have a restaurant object available to test our API responses.
```python
@classmethod
def setUpClass(cls):
    cls.restaurant_list_url = reverse('Restaurant-list')
    cls.client = APIClient()
    cls.res_data = {
        'restaurant_id': '27974',
        'restaurant_name': 'Cross Street Bar',
        'date_created': timezone.now(),
        'category_clickbacon_account_id_map': {},
        'category_quickbooks_account_id_map': {},
        'cash_in_registers_quickbooks_account_id': '',
        'quickbook_payment_accounts_mapping': {}
    }
    cls.restaurant = Restaurant.objects.create(**cls.res_data)
```

### 2. **Testing Model Creation**
This test checks whether the `Restaurant` model correctly creates an instance with the given attributes.

**Example:**
```python
def test_create_restaurant(self):
    # Checking if the restaurant instance is created correctly
    self.assertTrue(isinstance(self.restaurant, Restaurant))
    # Verifying the string representation
    self.assertEqual(self.restaurant.__str__(), "Cross Street Bar || 27974")
    # Ensuring the restaurant exists in the database
    self.assertTrue(Restaurant.objects.filter(restaurant_id='27974').exists())
```

### 3. **Testing GET Requests**
This test verifies that the restaurant list API endpoint returns the expected data when a GET request is made.

**Example:**
```python
def test_restaurant_list_view(self):
    response = self.client.get(self.restaurant_list_url)
    # Ensuring the API responds with 200 OK
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    # Checking if the response contains expected restaurant details
    self.assertContains(response, 'Cross Street Bar')
    self.assertContains(response, '27974')
```

### 4. **Testing POST Requests**
This test ensures that new restaurants can be created using the API.

**Example:**
```python
def test_create_restaurant_api(self):
    new_restaurant_data = {
        'restaurant_id': '27976',
        'restaurant_name': 'New Place',
        'date_created': timezone.now()
    }
    response = self.client.post(self.restaurant_list_url, new_restaurant_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertTrue(Restaurant.objects.filter(restaurant_id='27976').exists())
```

### 5. **Testing PUT Requests**
This test verifies that an existing restaurant's data can be updated using the API.

**Example:**
```python
def test_update_restaurant_api(self):
    update_data = {
        'restaurant_name': 'Updated Cross Street Bar'
    }
    update_url = reverse('Restaurant-detail', kwargs={'pk': self.restaurant.restaurant_id})
    response = self.client.put(update_url, update_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.restaurant.refresh_from_db()
    self.assertEqual(self.restaurant.restaurant_name, 'Updated Cross Street Bar')
```

### 6. **Testing API Responses with Filters**
This test ensures that filtering functionality works correctly when querying the API with specific parameters.

**Example:** Filtering by restaurant name.
```python
def test_restaurant_list_api_filter_by_name(self):
    response = self.client.get(self.restaurant_list_url, {'restaurant_name': 'Cross Street Bar'})
    # Checking if the response returns 200 OK
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    # Ensuring only the expected restaurant is returned
    self.assertEqual(len(response.data['data']), 1)
    self.assertEqual(response.data['data'][0]['restaurant_name'], 'Cross Street Bar')
```

### 7. **Testing Invalid API Requests**
This test verifies that the API correctly handles invalid filter parameters by returning an appropriate error message.

**Example:**
```python
def test_restaurant_list_api_invalid_filter(self):
    response = self.client.get(self.restaurant_list_url, {'invalid_param': 'value'})
    # Ensuring the response returns 400 Bad Request
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertIn("Invalid filter", response.data['message'])
```

### 8. **Testing Pagination in API Responses**
This test ensures that the API correctly paginates responses when multiple entries exist.

**Example:**
```python
def test_restaurant_list_api_pagination(self):
    # Creating an additional restaurant instance to test pagination
    restaurant2_data = {
        'restaurant_id': '27975',
        'restaurant_name': 'Another Restaurant',
        'date_created': timezone.now()
    }
    Restaurant.objects.create(**restaurant2_data)
    response = self.client.get(self.restaurant_list_url, {'page': 1, 'page_size': 1})
    # Checking if the API correctly limits results per page
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data['data']), 1)
```

## Best Practices for Unit Testing in Django

1. **Use `setUpClass()` or `setUp()`** to create reusable test data.
2. **Follow a consistent naming convention** for test methods (e.g., `test_<functionality>`).
3. **Use assertions effectively**, such as `assertEqual()`, `assertTrue()`, `assertContains()`, etc.
4. **Test edge cases** (e.g., no data, multiple records, invalid inputs).
5. **Test API filtering, pagination, and error handling**.
6. **Run tests frequently** using Django's built-in test runner: 
   ```sh
   python manage.py test
   ```
7. **Keep tests isolated** and avoid dependencies between test cases.
8. **Use `APITestCase`** for API tests to ensure proper client handling.

