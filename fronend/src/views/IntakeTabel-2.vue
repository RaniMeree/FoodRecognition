<template>
  <v-container>
    <NavBar>
      <div class="d-flex align-items-center">
        <!-- Date filter input -->
        <v-text-field
          v-model="dateFilter"
          label="Filter by Date"
          type="date"
          class="mb-4"
        ></v-text-field>

        <!-- Display requiredCalories value next to date filter -->
        <div class="ms-3">
          Required Calories: {{ requiredCalories }}
        </div>
      </div>
      <!-- Data table -->
      <v-data-table
        :headers="headers"
        :items="filteredItems"
        class="custom-table"
      ></v-data-table>
    </NavBar>
  </v-container>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import NavBar from '@/components/NavBar.vue';
import { useMainSysInfo } from '@/stores/main.js';
import { useRouter } from 'vue-router';

export default {
  components: {
    NavBar,
  },
  setup() {
    const sysInfo = useMainSysInfo();
    const router = useRouter();

    const dateFilter = ref('');
    const items = ref([]);
    const requiredCalories = ref(0); // Initialize requiredCalories ref

    // Headers for the data table
    const headers = [
      { text: 'Detected Food', value: 'Detected Food' },
      { text: 'Calories per gram', value: 'Calories per gram' },
      { text: 'Amount in grams', value: 'Amount in grams' },
      { text: 'Date', value: 'Date' },
      { text: 'Total Calories', value: 'Total Calories' },
    ];

    // Fetching data and calculating required calories on component mount
    onMounted(async () => {
      console.log('Response Data:', response.data);  
      try {
        const response = await axios.get('calories/intake', {
          headers: {
            token: localStorage.getItem('token'),
            'Content-Type': 'application/json',
          },
        });

        const reorderedData = response.data.map((item) => ({
          'Detected Food': item.food_name,
          'Calories per gram': item.food_calories,
          'Amount in grams': item.count,
          'Date': item.date,
          'Total Calories': item.count * item.food_calories,
        }));
        items.value = reorderedData;

        // Calculate required calories after fetching user data
        calculateRequiredCalories();
      } catch (error) {
        sysInfo.alert(error.response.data.detail, 'red', 2000);
      }
    });

    // Function to calculate required calories
    async function calculateRequiredCalories() {
      try {
        // Fetch user data from the backend
        const response = await axios.get('/api/user/profile', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });

        // Extract user data from the response
        const userData = response.data;

        // Extract user data required for calorie calculation
        const { weight, height, age, gender, activity, goal } = userData;
        console.log('User Data:', userData);

        // Calculate required calories based on user data
        let BMR;
        if (gender === 'Male') {
          BMR = 10 * weight + 6.25 * height - 5 * age + 5;
        } else if (gender === 'Female') {
          BMR = 10 * weight + 6.25 * height - 5 * age - 161;
        }

        // Multiply BMR by the activity level factor
        let dailyCalories = BMR * getActivityLevelFactor(activity);

        // Adjust calories based on the goal
        if (goal === 'Weight Loss') {
          dailyCalories *= 0.8; // Reduce by 20%
        } else if (goal === 'Weight Gain') {
          dailyCalories += 500; // Add 500 calories for weight gain
        }

        // Update requiredCalories value
        requiredCalories.value = dailyCalories.toFixed(2);
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    }

    // Helper function to get activity level factor
    function getActivityLevelFactor(activity) {
      switch (activity) {
        case 'No Exercise':
          return 1.2;
        case 'Once a week':
          return 1.4;
        case '2-3 times per week':
          return 1.6;
        case '4-5 times per week':
          return 1.8;
        default:
          return 1.2; // Default to sedentary activity level
      }
    }

    // Computed property for filtering items based on date
    const filteredItems = computed(() => {
      if (dateFilter.value) {
        return items.value.filter((item) => item.Date === dateFilter.value);
      }
      return items.value;
    });

    return {
      sysInfo,
      dateFilter,
      items,
      filteredItems,
      headers,
      requiredCalories,
    };
  },
};
</script>

<style>
/* Add any custom styling for the v-data-table */
.custom-table {
  /* Customize the table as you prefer */
}
</style>
