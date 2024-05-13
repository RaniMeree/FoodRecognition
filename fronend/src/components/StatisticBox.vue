<script>
import { ref, onMounted, defineProps  } from 'vue';
  export default {

    props: {
        title: {
        type: String,
        default: 'title',
        },
        number: {
        type: String,
        default: '0',
        },
        color: {
        type: String,
        default: '#1A237E',
        },
    },

    setup(props) {
        
        return{
            title: props.title,
            number: props.number,
            color: props.color,

        }
    }
  }
</script>

<template>
<div v-directiv="{ height: '100px' }" class="v-col-md-3 v-col-sm-6 v-col-12 d-flex align-center ga-3 bg-white" >
    <div  >
        <v-btn  :color="color" size="small" icon="$vuetify" variant="tonal">
        </v-btn>
    </div>
    <div >
        <p class="text-subtitle-2 font-weight-black">{{number}}</p>
        <p class="text-subtitle-2 font-light">{{ title }}</p>
    </div>
</div>
</template>

<style>

</style>
