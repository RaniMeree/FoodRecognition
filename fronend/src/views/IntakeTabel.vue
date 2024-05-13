<template>
  <NavBar>
    <div>
      <h1>Your Daily Calories: {{ requiredCalories }}</h1>
      
      <h1>Total Consumed Calories: {{ totalCalories }}</h1>  </div>
      <v-data-table :items="items" :headers="headers"></v-data-table>
  </NavBar>
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

    const items = ref([]);
    const requiredCalories = ref(0); // State variable for required calories

    // Headers for the data table
    const headers = [
      { text: 'Detected Food', value: 'Detected Food' },
      { text: 'Calories per gram', value: 'Calories per gram' },
      { text: 'Amount in grams', value: 'Amount in grams' },
      { text: 'Date', value: 'Date' },
      { text: 'Total Calories', value: 'Total Calories' },
    ];

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

        const requiredCaloriesResponse = await axios.get(
          '/users/profile',
          {
            headers: {
              token: localStorage.getItem('token'),
              'Content-Type': 'application/json',
            },
          }
        );

        console.log('Fetched required calories:', requiredCaloriesResponse.data.requiredCalories);

        requiredCalories.value = requiredCaloriesResponse.data.requiredCalories;
      } catch (error) {
        console.error('Error fetching required calories:', error);
      }
    });

    const totalCalories = computed(() => {
      // Calculate total calories from all items
      return items.value.reduce((acc, item) => acc + item['Total Calories'], 0);
    });

    return {
      sysInfo,
      items,
      requiredCalories,
      totalCalories,
    };
  },
};
</script>

<style>
  /* Add styling for the h1 element if needed */
</style>
