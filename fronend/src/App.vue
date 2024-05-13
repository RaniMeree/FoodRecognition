<script >
import { RouterLink, RouterView, useRouter  } from 'vue-router'
import { ref, onMounted } from 'vue';
import { useMainSysInfo } from '@/stores/main.js';
import { useUserInfo } from '@/stores/userInfo.js';
export default {

  setup() {
    const sysInfo = useMainSysInfo()
    const userInfo = useUserInfo()
    const router = useRouter();
    onMounted(() => {
      if(!localStorage.getItem('token')){
        router.push({ name: 'signup' });
      }
      userInfo.username = localStorage.getItem('username')
    });

    return {
      sysInfo,
        }
    
      }
}

</script>

<template>
  <v-app :class="{ 'background-light-color': sysInfo.isDarkTheme, 'background-dark-color': !sysInfo.isDarkTheme }">

    <!-- <v-btn icon="$vuetify" @click="sysInfo.isDarkTheme = !sysInfo.isDarkTheme">
      Button
    </v-btn> -->

    <v-snackbar
    id="main_alert"
    :color="sysInfo.alertColor"
    v-model="sysInfo.alertStatus"
    :timeout="sysInfo.alertTime" >
      <p class="text-center font-weight-bold">
        {{ sysInfo.alertMessage }}
      </p>
    </v-snackbar>

    <router-view  v-slot="{ Component }">
    <transition name="route" mode="out-in">
      <component :is="Component" />
    </transition>
  </router-view>



  </v-app>
</template>

<style >
#main_alert{
  bottom: 87.5% !important;
}

.route-enter-from{
  opacity: 0;
  /* transform: translateX(100px); */
}
.route-enter-active{
  transition: all 0.3s ease-out;
}

.route-leave-to{
  opacity: 0;
  transform: translateX(100px);
}

.route-leave-active {
  transition: all 0.3s ease-in;
}

</style>
