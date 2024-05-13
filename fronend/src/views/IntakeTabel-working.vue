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

        <!-- Display adjustedCalories value next to date filter -->
        <div class="ms-3">
          Adjusted Calories: {{ requiredCalories }}
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
    function calculateRequiredCalories() {
      // Replace these values with actual user data
      const weight = 70; // Example weight in kg
      const height = 170; // Example height in cm
      const age = 30; // Example age
      const gender = 'Male'; // Example gender
      const activityLevel = 1.6; // Example activity level
      const goal = 'Maintain Weight'; // Example goal

      let BMR;
      if (gender === 'Male') {
        BMR = 10 * weight + 6.25 * height - 5 * age + 5;
      } else if (gender === 'Female') {
        BMR = 10 * weight + 6.25 * height - 5 * age - 161;
      }

      // Multiply BMR by the activity level factor
      let dailyCalories = BMR * activityLevel;

      // Adjust calories based on the goal
      if (goal === 'Weight Loss') {
        dailyCalories *= 0.8; // Reduce by 20%
      } else if (goal === 'Weight Gain') {
        dailyCalories += 500; // Add 500 calories for weight gain
      }

      requiredCalories.value = dailyCalories.toFixed(2);
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
