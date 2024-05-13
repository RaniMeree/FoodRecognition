<script>
import { ref,watch } from 'vue'
import {inputsValidation} from '@/assets/js/main.js'
import { useMainSysInfo } from '@/stores/main.js';
import { useUserInfo } from '@/stores/userInfo.js';
import axios from 'axios';
import { useRouter } from 'vue-router'
export default {
  
  setup() {
    
    const router = useRouter();
    const sysInfo = useMainSysInfo()
    const userInfo = useUserInfo()

    const localInputsRules = {
    rePass : value => value === password.value || 'password does not match'
}

    const password = ref('')
    const registerData = ref({
      username:{value:'',validation:{
        required:true,
        minLen:'',
        maxLen:'',
        regex:'',
        lookalike:'',
      }},
      email:{value:'',validation:{
        required:true,
        minLen:'',
        maxLen:'',
        regex:'email',
        lookalike:'',
      }},
      weight:{value:'',validation:{
        required:true,
        minLen:'',
        maxLen:'',
        regex:'',
        lookalike:'',
      }},
      height:{value:'',validation:{
        required:true,
        minLen:'',
        maxLen:'',
        regex:'',
        lookalike:'',
      }},
      age:{value:'',validation:{
        required:true,
        minLen:'',
        maxLen:'',
        regex:'',
        lookalike:'',
      }},
      gender:{value:'',validation:{
        required:true,
        minLen:'',
        maxLen:'',
        regex:'',
        lookalike:'',
      }},
      activity:{value:'',validation:{
        required:true,
        minLen:'',
        maxLen:'',
        regex:'',
        lookalike:'',
      }},
      goal: {
      value: '',
      validation: {
        required: true,
        minLen: '',
        maxLen: '',
        regex: '',
        lookalike: '',
      },
    },
      password:{value:'',validation:{
        required:true,
        minLen:'6',
        maxLen:'',
        regex:'',
        lookalike:'',
      }},
      rePassword:{value:'',validation:{
        required:true,
        minLen:'6',
        maxLen:'',
        regex:'',
        lookalike:'',
      }},
    })

    var visiblePass = ref(false)
    var visibleRePass = ref(false)
    const goalChoices = ['maintain weight', 'lose weight', 'gain weight'];
    const genderChoices = ['Male', 'Female'];
    const activityChoices = ['No Exercise', 'Once a week', '2-3 times per week', '4-5 times per week'];

    const rules = sysInfo.inputsRules

    const signup = async () => {
    // Validate input data and get requestData
    const requestData = inputsValidation(registerData.value, ['rePassword']);
    
    if (requestData) {
        // Calculate adjusted calories based on user inputs
        

        try {
            // Send signup request
            const response = await fetch(`${sysInfo.backendBaseURL}users/authentication/signup`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify(requestData),
            });

            if (!response.ok) {
                const errorData = await response.json();
                sysInfo.alert(errorData.detail, 'red', 2000);
                return;
            }

            // Process response and navigate to home
            const responseData = await response.json();
            localStorage.setItem('token', responseData.token);
            localStorage.setItem('username', responseData.username);
            userInfo.username = responseData.username;
            userInfo.is_auth = true;
            router.push({ name: 'home' });

        } catch (error) {
            console.error('Error:', error);
        }
    }
};


    
    watch(() => password.value, (newValue, oldValue) => {
      registerData.value.password.value = newValue
      registerData.value.rePassword.validation.lookalike = newValue
    })

    return {
      router,
      sysInfo,
      localInputsRules,
      registerData,
      password,
      rules,
      signup,
      visiblePass,
      visibleRePass,
      genderChoices,
      activityChoices,
      goalChoices,
    }

  },

  mounted() {

  }

}


function calculateBMI(weight, height) {
        return weight / ((height / 100) ** 2);
    }

    // Function to calculate required calories
    function calculateRequiredCalories(weight, height, age, gender, activity, goal) {
        let BMR;
        if (gender === 'Male') {
            BMR = 10 * weight + 6.25 * height - 5 * age + 5;
        } else {
            BMR = 10 * weight + 6.25 * height - 5 * age - 161;
        }

        const activityLevels = {
            'No Exercise': 1.2,
            'Once a week': 1.4,
            '2-3 times per week': 1.6,
            '4-5 times per week': 1.8,
        };

        const goalAdjustments = {
            'maintain weight': 0,
            'lose weight': -0.2, // Reduce by 20%
            'gain weight': 0.5, // Add 500 calories
        };

        const activityFactor = activityLevels[activity] || 1;
        const goalAdjustment = goalAdjustments[goal] || 0;

        let dailyCalories = BMR * activityFactor;

        if (goal === 'lose weight') {
            dailyCalories *= 0.8; // Reduce by 20%
        } else if (goal === 'gain weight') {
            dailyCalories += 500; // Add 500 calories
        }

        return dailyCalories;
    }

</script>

<template>
  <v-container>    
    <div class="register-page" style="height: 100% ;">
      <div class="register-box">
        <div class="register-box-header">
          <h3 :class="{ 'light-color': sysInfo.isDarkTheme, 'dark-color': !sysInfo.isDarkTheme }">
            Create New Account
          </h3>
          <p>
            Create an account and monitor your calorie intake
          </p>
        </div>
        <div class="register-box-inputs">
          <v-form @submit.prevent="signup()">
  
            <v-text-field 
            label="Username" 
            variant="outlined"
            hint="enter your name"
            :rules="[rules.required]"
            v-model="registerData.username.value"
            :color="sysInfo.inputsColor"
            ></v-text-field>
  
            <v-text-field 
            label="Email" 
            variant="outlined"
            hint="enter your name"
            :rules="[rules.required,rules.email]"
            v-model="registerData.email.value"
            :color="sysInfo.inputsColor"
            ></v-text-field>
  
            <div class="d-flex justify-space-between">

              <div class="w-33"> 
                <v-text-field 
                  label="Weight" 
                  variant="outlined"
                  hint="enter your weight"
                  :rules="[rules.required]"
                  v-model="registerData.weight.value"
                  :color="sysInfo.inputsColor"
                ></v-text-field>
              </div>

              <div class="w-33"> 
                <v-text-field 
                  label="Height" 
                  variant="outlined"
                  hint="enter your height"
                  :rules="[rules.required]"
                  v-model="registerData.height.value"
                  :color="sysInfo.inputsColor"
                ></v-text-field>
              </div>

              <div class="w-33"> 
                <v-text-field 
                  label="Age" 
                  variant="outlined"
                  hint="enter your age"
                  :rules="[rules.required]"
                  v-model="registerData.age.value"
                  :color="sysInfo.inputsColor"
                ></v-text-field>
              </div>



            </div>
  
            <div class="v-row ">
                <v-text-field
                class="v-col-sm-6 v-col-12 ma-0"
                :append-inner-icon="visiblePass ? 'mdi-eye' : 'mdi-eye-off'"
                label="Password"
                :type="visiblePass ? 'text' : 'password'"
                prepend-inner-icon="mdi-lock-outline"
                variant="outlined"
                @click:append-inner="visiblePass = !visiblePass"
                :rules="[rules.required,rules.pass]"
                v-model="password"
                :color="sysInfo.inputsColor"
              ></v-text-field>
  
              <v-text-field
              class="v-col-sm-6 v-col-12 ma-0"
              :append-inner-icon="visibleRePass ? 'mdi-eye' : 'mdi-eye-off'"
              label="Rewrite password"
              :type="visibleRePass ? 'text' : 'password'"
              prepend-inner-icon="mdi-lock-outline"
              variant="outlined"
              @click:append-inner="visibleRePass = !visibleRePass"
              :rules="[rules.required,localInputsRules.rePass]"
              v-model="registerData.rePassword.value"
              :color="sysInfo.inputsColor"
              ></v-text-field>
            </div>
            <v-select
              label="Gender"
              :items="genderChoices"
              variant="outlined"
              :rules="[rules.required]"
              v-model="registerData.gender.value"
              :color="sysInfo.inputsColor"
            ></v-select>

            <v-select
              label="Activity"
              :items="activityChoices"
              variant="outlined"
              :rules="[rules.required]"
              v-model="registerData.activity.value"
              :color="sysInfo.inputsColor"
            ></v-select>
            
            <v-select
              label="Goal"
              :items="goalChoices"
              variant="outlined"
              :rules="[rules.required]"
              v-model="registerData.goal.value"
              :color="sysInfo.inputsColor"
            ></v-select>



            <v-btn block size="large" :color="sysInfo.buttonColor"  type="submit" class="mt-8 ">
              SignUp
            </v-btn>
  
          </v-form>
          <div class="peimary-color mt-5">
            <router-link :to="{ name: 'login' }">I Have Account!</router-link>
          </div>
        </div>
      </div>
    </div>
  </v-container>
</template>

<style>
#phoneCode .v-field__append-inner{
  display: none !important;
}
</style>