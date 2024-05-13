<template>
  <NavBar>

    <v-dialog
      v-model="dialog"
      width="auto"
    >
      <v-card
        max-width="400"
        prepend-icon="mdi-food"
        text="Enter the amount of food you ate in grams."
        title="Intake Amount"
      >
      <v-text-field
        type="number"
        style="padding: 16px 24px 10px;"
        label="intake amount"
        variant="underlined"
        :rules="[rules.required]"
        v-model="intake_count"
        :color="sysInfo.inputsColor"
        :style="{
          'color': sysInfo.isDarkTheme ? `${sysInfo.input_outline_light_color} !important` : `${sysInfo.input_outline_dark_color} !important` ,
        }"
      ></v-text-field>

        <template v-slot:actions>
          <v-btn
            class="ms-auto me-auto"
            text="Ok"
            @click="calories_calculation()"
          ></v-btn>
        </template>
      </v-card>
    </v-dialog>

    <div class="d-flex justify-center align-center">
      <div class="d-flex align-center" style="gap: 10px;">
        <p style="font-size: x-large;" class="">Camera</p>
        <v-switch v-model="uploadType" hide-details></v-switch>
        <p style="font-size: x-large;" class="">Upload</p>
      </div>
    </div>
    <div v-if="!processing" class="d-flex justify-center align-center h-100">
      <div v-if="uploadType" id="upload-image-secion" class="">
        <div class="upload-bg">
          <v-icon color="#ffffff" icon="mdi-tray-arrow-up" size="100px" @click="upload_input()"></v-icon>
          <input type="file" name="" id="" hidden ref="photo_input" @change="sendPhoto($event.target.files[0],'upload')">
        </div>
      </div>
      <div v-else id="camera-secion">
        <video id="camera-screen" ref="videoElement" autoplay></video>
        <div class="d-flex justify-space-between mt-7" style="gap: 18px;">
          <v-btn v-if="cameraIsOpen" @click="takePhoto" color="#1565C0" prepend-icon="mdi-camera-plus" style="width: 49%;">
            Take photo
          </v-btn>
          <v-btn v-if="cameraIsOpen" color="#1565C0" @click="stopCamera" prepend-icon="mdi-camera-lock" style="width: 49%;">
            Close camera
          </v-btn>
          <v-btn v-else @click="startCamera" color="#1565C0" prepend-icon="mdi-webcam" style="width: 100%;">
            Open camera
          </v-btn>
        </div>
      </div>
    </div>
    <div v-else class="d-flex justify-center align-center h-100">
      <v-progress-circular
      :size="100"
      color="#1565C0"
      indeterminate
      ></v-progress-circular>
    </div>
  </NavBar>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';
import NavBar from '@/components/NavBar.vue';
import { useMainSysInfo } from '@/stores/main.js';
import { useRouter } from 'vue-router'
export default {
  components: {
    NavBar,
  },
  setup() {
    const router = useRouter();
    const sysInfo = useMainSysInfo()
    const rules = sysInfo.inputsRules
    const stream = ref(null);
    const uploadType = ref(false);
    const cameraIsOpen = ref(false);
    const videoElement = ref(null);
    const photo_input = ref(null);
    const calorie = ref(null);
    const dialog = ref(false);
    const intake_count = ref(null)
    const processing = ref(false)

    
    const upload_input = () => {
      photo_input.value.click();
    }

    const startCamera = async () => {
      try {
        cameraIsOpen.value = true;
        const streamVal = await navigator.mediaDevices.getUserMedia({ video: true });
        stream.value = streamVal;
        videoElement.value.srcObject = streamVal;
      } catch (error) {
        console.error('Error accessing camera:', error);
      }
    };

    const stopCamera = () => {
      if (stream.value) {
        cameraIsOpen.value = false;
        stream.value.getTracks().forEach(track => track.stop());
        videoElement.value.srcObject = null;
        stream.value = null;
      }
    };

    const takePhoto = async () => {
      if (!stream.value) {
        console.error('Camera not started.');
        return;
      }
      
      const canvas = document.createElement('canvas');
      canvas.width = videoElement.value.videoWidth;
      canvas.height = videoElement.value.videoHeight;
      canvas.getContext('2d').drawImage(videoElement.value, 0, 0, canvas.width, canvas.height);
      const imageDataUrl = canvas.toDataURL('image/jpeg');

      sendPhoto(imageDataUrl, 'camera');
    };

    const calories_calculation = async () => {
        const data = {food_id: calorie.value.id, intake_count: intake_count.value}
        try {
        const response = await axios.post('calories/calculation', data, {
          headers:{
        token:localStorage.getItem('token'),
        'Content-Type': 'application/json'
        }
      });
        const responseData = response.data;
        router.push({ name: 'intake' });
        console.log(responseData)
        } catch (error) {
          sysInfo.alert(error.response.data.detail,'red',2000)
        }
    }

    const sendPhoto = async (imageData, fromType) => {
      try {
        if(fromType == 'camera'){
          const blob = await fetch(imageData).then(response => response.blob());
          var formData = new FormData();
          formData.append('file', blob, 'photo.jpg');
        }
        else{
          const file = imageData;
          var formData = new FormData();
          formData.append('file', file); 
        }

        processing.value = true
        const response = await axios.post('calories/food-photo', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            token:localStorage.getItem('token')
          },
        });

        if (response.status === 200) {
          console.log('Photo successfully sent.');
          console.log(response.data.calorie);
          calorie.value = response.data
          console.log(response.data)
          dialog.value = true
          processing.value = false
          
        } else {
          console.error('Failed to send photo:', response.statusText);
          processing.value = false
        }
      } catch (error) {
        sysInfo.alert(error.response.data.detail,'red',5000)
        console.error('Error sending photo:', error);
        processing.value = false
      }
    };

    return {
      sysInfo,
      rules,
      stream,
      uploadType,
      cameraIsOpen,
      videoElement,
      photo_input,
      dialog,
      intake_count,
      processing,
      sendPhoto,
      startCamera,
      stopCamera,
      takePhoto,
      upload_input,
      calories_calculation
    };
  },
};
</script>

<style>
#camera-secion {
  min-width: 50% !important;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

#upload-image-secion div {
  width: 250px;
}

#upload-image-secion img {
  width: 100%;
}

.v-switch__track {
  background-color: #1565C0;
}

.v-switch__thumb {
  background-color: #1565C0 !important;
  color: #1565C0;
}

#camera-screen {
  border-radius: 20px;
}

.upload-bg {
  background-color: rgba(21, 101, 192);
  display: flex;
  justify-content: center !important;
  transition: 0.3s;
  height: 200px;
  width: 200px !important;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}

.upload-bg:hover {
  background-color: rgba(21, 101, 192, 0.750);
}
</style>
