<template>
  <div class="container">
    <div>
      <div class="form-group">
        <label>Name</label>
        <input type="text" v-model="name" class="form-control" />
        {{ name }}
      </div>
      <div class="form-group">
        <label>Email</label>
        <input type="email" v-model="email" class="form-control" />
        {{ email }}
      </div>
      <div class="form-group">
        <label>Password</label>
        <input type="password" v-model="password" class="form-control" />
        {{ password }}
      </div>
      <div class="form-group">
          <button class="btn btn-primary" @click="login">Login</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Login",
  components: {},
  data() {
    return {
      name: "",
      password: "",
      email: "",
    };
  },
  methods: {
      login(){
          fetch(
              'http://127.0.0.1:5000/api-login',
              {
                  "Content-Type": 'application/json',
                  "data": JSON.stringify(
                      {
                          "name": this.name,
                          "email": this.email,
                          "password": this.passwor,
                      }
                  )

              }

          ).then(e=>e.json()).then(e => alert(e));
          
          
      }
  }
};
</script>

<style>
</style>