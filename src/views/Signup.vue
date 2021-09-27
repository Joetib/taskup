<template>
  <div class="container py-5" style="max-width: 500px;margin-bottom:60vh">
    <form @submit.prevent="signup">
      <div>
        <h3 id="hding">Enter details to Sign Up</h3>
        <p class="lead">so we can show you that world you dream of . . . </p>
        <div id="fixerr" class=" p-2 rounded btn btn-outline-danger text-danger" v-if="error">
          {{ error }}
        </div>
        <div class="form-group py-2">
          <label>Name</label>
          <input id="id1_0" type="text" placeholder="Enter your name" v-model="name" class="form-control" required minlength="3"/>
        </div>
        <div class="form-group py-2">
          <label>Email</label>
          <input id="id1" placeholder="Enter a valid mail" type="email" v-model="email" class="form-control" required/>
        </div>
        <div class="form-group py-2">
          <label>Password</label>
          <input id="id1_1" placeholder="Your Password" type="password" v-model="password" class="form-control" required minlength="5"/>
        </div>
        <div class="form-group py-2">
          <button class="btn btn-primary" @click="signup">Sign Up</button>
        </div>
        <div class="form-group">
          <br><br>
          <p id="link1_1">
            Please <router-link id="link1" to="/login"><span id="link1_11"> Log In </span></router-link> if you already
            have an account.
          </p>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Login",
  components: {},
  data() {
    return {
      name: "",
      password: "",
      email: "",
      error: "",
    };
  },
  methods: {
    signup() {   
      this.error = null
      
      const name = document.getElementById("id1_0");
      const email = document.getElementById("id1");
      const password = document.getElementById("id1_1");

      if(name.checkValidity() && email.checkValidity() && password.checkValidity()){
        this.$store.commit("setIsLoading", true);
        axios
          .post("/auth/signup/", {
            name: this.name,
            email: this.email,
            password: this.password,
          })
          .then((e) => {
            if (e.data.success) {
              this.username = e.data.name;
              this.token = e.data.token;
              this.$store.commit("updateUsername", e.data.name);
              this.$store.commit("updateToken", e.data.token);
              this.$store.commit("updateEmail", e.data.email);
              this.$store.commit("setIsLoading", false);

              if (this.$route.params.nextUrl == null) {
                this.$router.push("/dashboard");
              } else {
                this.$router.push(this.$route.params.nextUrl);
              }
            }else {
                this.error = e.data.message;
                this.$store.commit("setIsLoading", false);
            }
          })
          .catch((e) => {
            this.error =
              "Sorry, an error occured! Try again";
            console.log(e);
            this.$store.commit("setIsLoading", false);
          });
      }
  } 
  },
  };

</script>

<style scoped>

.btn-primary{
  border-radius: 10px;
  font-family: montserrat;
  margin-left: .2em;
  margin-top: 1em;
  font-size: 1.2em;
  font-weight: bold;
}

#fixerr{
  background: transparent !important;
  position:relative;
  width: 100%;
  margin: auto;
  font-weight: bold;
}
.container{
  border-radius: 2em;
  margin-top: 50px;
  padding-left: 2em;
  padding-right: 2em;
  margin-bottom: 4.5em;
}

#link1_1{
  text-align: center;
  font-family: Arial, Helvetica, sans-serif;
}

#link1_11{
  font-size: 1.4em;
  font-weight: bold;
  color: #1275d8;
}

#hding{
  color: #2e2d2de0;
}
@media screen and (min-width: 770px) {
  .container{
  background-color:rgba(97, 78, 78, 0.15);
}
}
</style>
