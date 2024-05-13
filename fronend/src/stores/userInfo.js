import { defineStore } from 'pinia'
import axios from 'axios';

export const useUserInfo = defineStore('userInfo', {

  state:() => ({
    userInfo:{
      username:'',
      is_auth: false,
      companyName:'',
      email:'',
      phone:'',
      companyType:'',
      phoneCode:'',
    }
  }),

  actions:{
    async signup(requestData){        
        // dasd@asd.sddd
        this.userInfo = requestData
        // try{
        //   const response = await axios.post('http://127.0.0.1:4040/api/user/sign_up', requestData ,{
        //     headers: {'Authorization': 'E2pyOL1PEHAeytDmZdkVRWqFTBaXGA'},
        //     credentials: 'include',});
        //   console.log('Response:', response.data);
        //   this.userInfo = response.data
        // }
        // catch(error){
        //   console.error('Error:', error);
        // }
    }
  }

})
