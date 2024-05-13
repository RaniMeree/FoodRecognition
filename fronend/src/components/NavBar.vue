<script>
import { ref, onMounted } from 'vue';
import { useUserInfo } from '@/stores/userInfo.js';

  export default {
    setup() {
        const userInfo = useUserInfo()
        const drawer =  ref(true)
        const rail =  ref(false)

        const logout = () => {
          localStorage.removeItem('token')
          router.push({ name: 'signup' });
        }
        
        return{
            drawer,
            rail,
            userInfo,
            logout
        }
    }
  }
</script>

<template>
    <v-card >
      <v-layout>
        <v-navigation-drawer
          location="left"
          v-model="drawer"
          :rail="rail"
          permanent
        >
          <v-list-item
          prepend-avatar="https://cdn-icons-png.flaticon.com/512/3541/3541871.png"
            :title='userInfo.username'
            nav
          >
            <template v-slot:append>
              <v-btn
                variant="text"
                icon="mdi-chevron-left"
                @click.stop="rail = !rail"
              ></v-btn>
            </template>
          </v-list-item>

          <v-list v-if="rail === true" density="compact" nav>
            <v-btn  variant="text" @click="rail = false" density="comfortable" icon="mdi-chevron-right"></v-btn>
          </v-list>

          <v-divider></v-divider>
  
          <v-list density="compact" nav>

            <router-link  :to="{ name: 'home' }" class="un-active" exact-active-class="active" active-class="active">
              <v-list-item prepend-icon="mdi-home-account" title="Home" value="home"></v-list-item>
          </router-link>

            <router-link  :to="{ name: 'intake' }" class="un-active" exact-active-class="active" active-class="active">
              <v-list-item prepend-icon="mdi-food" title="Intake" value="Intake"></v-list-item>
          </router-link>

          <!-- <v-list-group value="pro-mg">
            <template v-slot:activator="{ props }">
              <v-list-item
              :class="$route.fullPath.includes('offers') || $route.fullPath.includes('turkr_store_products') ? 'active' : 'un-active'"
              v-bind="props"
              prepend-icon="mdi-store"
              title="XXX"
              ></v-list-item>
            </template>

          </v-list-group> -->

          <router-link  to="/signup" class="un-active" exact-active-class="active" active-class="active" @click="logout()">
                <v-list-item prepend-icon="mdi-login" title="logout" value="Logout"></v-list-item>
          </router-link>

            <!-- <router-link  to="/signup" class="un-active" exact-active-class="active" active-class="active">
                <v-list-item prepend-icon="mdi-login" title="signup" value="SignUp"></v-list-item>
            </router-link>
            <router-link  to="/login" class="un-active" exact-active-class="active" active-class="active">
                <v-list-item prepend-icon="mdi-account-plus" title="Login" value="signup"></v-list-item>
            </router-link> -->

          </v-list>
        </v-navigation-drawer>
        <v-main class="peimary-bg-color" style="min-height: calc(100vh)!important;">
            <slot></slot>
        </v-main>
      </v-layout>
    </v-card>
  </template>

<style >

.active{
color: #1565C0  !important;
text-decoration: none;

}
.active .v-list-item__overlay{
  opacity: 0.1 !important;
} 

.un-active{
color: rgba(0,0,0,.87) ;
text-decoration: none;

}

</style>