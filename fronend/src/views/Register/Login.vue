<script>
import { ref,watch } from 'vue'
import {inputsValidation} from '@/assets/js/main.js'
import { useMainSysInfo } from '@/stores/main.js';
import { useUserInfo } from '@/stores/userInfo.js';
import { useRouter } from 'vue-router'


import axios from 'axios';
export default {
  
  setup() {

    const sysInfo = useMainSysInfo()
    const userInfo = useUserInfo()
    const router = useRouter();
    
    const registerData = ref({
      email:{value:'',validation:{
        required:true,
        len:'',
        regex:'email',
        lookalike:'',
      }},
      password:{value:'',validation:{
        required:true,
        len:'',
        regex:'',
        lookalike:'',
      }},
    })

    var visiblePass = ref(false)
    const rules = sysInfo.inputsRules

    const login = async () => {
      var requestData = inputsValidation(registerData.value)
      if(requestData){
        const formData = {password: requestData.password,email: requestData.email};
        // formData.append('username', requestData.email);
        // formData.append('password', requestData.password);
        // try {
        // const response = await axios.post('user/login', formData, {
        //   // withCredentials: true,
        // });
        // const responseData = response.data;
        // console.log(responseData)
        // } catch (error) {
        //   sysInfo.alert(error.response.data.detail,'red',2000)
        // }
        try {
          
          const response = await fetch(`${sysInfo.backendBaseURL}users/authentication/login`, {
            method: 'POST',
            headers: {
                  'Content-Type': 'application/json',
                },
          credentials: 'include',
          body: JSON.stringify(formData),
          });
          if (!response.ok) {
            const errorData = await response.json();
            sysInfo.alert(errorData.detail,'red',2000)
            return;
          }     
          const responseData = await response.json();
          localStorage.setItem('token', responseData.token);
          localStorage.setItem('username', responseData.username);
          userInfo.username = responseData.username
          userInfo.is_auth = true
          router.push({ name: 'home' });
        }
        catch (error) {
              console.error('Error:', error);
        }

      }

    }
    
    return {
      sysInfo,
      registerData,
      rules,
      login,
      visiblePass,
      userInfo,

    }

  },
  mounted() {

  }

}

</script>

<template>
  <v-container>
    <div class="register-page" style="height: 100% !important ;">
      <div class="register-box" :class="{ 'section-light-color': sysInfo.isDarkTheme, 'section-dark-color': !sysInfo.isDarkTheme }">
        <div class="register-box-header">
          <h3 :class="{ 'light-color': sysInfo.isDarkTheme, 'dark-color': !sysInfo.isDarkTheme }">
            login
          </h3>
          <p>
              <!-- تسجيل الدخول إلى حسابك على منصة تجارة تك -->
          </p>
        </div>
        <div class="register-box-inputs">
          <v-form @submit.prevent="login()">
  
          <v-text-field 
            label="Email" 
            variant="outlined"
            :rules="[rules.required,rules.email]"
            v-model="registerData.email.value"
            :color="sysInfo.inputsColor"
            :style="{
              'color': sysInfo.isDarkTheme ? `${sysInfo.input_outline_light_color} !important` : `${sysInfo.input_outline_dark_color} !important` ,
            }"
          ></v-text-field>
  
          <v-text-field
              class=" ma-0"
              :append-inner-icon="visiblePass ? 'mdi-eye' : 'mdi-eye-off'"
              label="Password"
              :type="visiblePass ? 'text' : 'password'"
              prepend-inner-icon="mdi-lock-outline"
              variant="outlined"
              @click:append-inner="visiblePass = !visiblePass"
              :rules="[rules.required]"
              v-model="registerData.password.value"
              :color="sysInfo.inputsColor"
              :style="{
                'color': sysInfo.isDarkTheme ? `${sysInfo.input_outline_light_color} !important` : `${sysInfo.input_outline_dark_color} !important` ,
              }"
          ></v-text-field>
  
            <v-btn block size="large" :color="sysInfo.inputsColor"  type="submit" class="mt-8">
              Login
            </v-btn>
  
          </v-form>
          <div class="peimary-color mt-5">
              <router-link :to="{ name: 'signup' }">I don not have account</router-link>
          </div>
        </div>
      </div>
    </div>
  </v-container>
</template>

<style>

</style>