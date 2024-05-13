import './assets/style/main.css'
import './assets/js/main.js'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'


const vuetify = createVuetify({
    components,
    directives
})


import axios from 'axios';
axios.defaults.baseURL = 'http://127.0.0.1:8000/api/';

import App from './App.vue'
import router from './router'

const app = createApp(App)

import CustomDirective from './directives';

app.directive('directiv', CustomDirective);

import VueApexCharts from "vue3-apexcharts";

app.use(createPinia())
app.use(router)
app.use(vuetify)
app.use(VueApexCharts)

app.mount('#app')

