import { defineStore } from 'pinia'

export const useMainSysInfo = defineStore('mainSysInfo', {

  state:() => ({

    backendBaseURL : 'http://127.0.0.1:8000/api/',
    
    isDarkTheme:true,

    alertStatus:false,
    alertMessage:'Message',
    alertColor:'red',
    alertTime:2000,
    
    buttonColor: '#1565C0',
    inputsColor: '#1565C0',
    color: '#1A237E',
    input_outline_color: 'black',
    section_color: 'white',
    background_color: '#eef2f6',


    inputsRules : {
      required: value => !!value || 'Required field',
      email: value => {
          const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
          return pattern.test(value) || 'invalid email'
        },
      pass: value => value.length > 5 || 'weak password',
      rePass : value => value === registerData.value.password.value || 'password does not match'
    }

  }),

  actions:{
    alert(message,color,time){        
      this.alertStatus = true
      this.alertMessage = message
      this.alertColor = color
      this.alertTime = time
    }
  }

})
