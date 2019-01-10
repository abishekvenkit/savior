<template>
  <div class="sign-up">
    <h3>Create a new account!</h3>
    <input type="text" placeholder="Email"><br>
    <input type="password" placeholder="Password"><br>
    <button>Sign Up</button>
    <p>Or go back to  <router-link to="/login">login</router-link></p>
  </div>
</template>

<script>
  export default {
    name: 'signUp',
    data() {
      return {}
    },
    methods: {}
  }
</script>

<style scoped>  /* "scoped" attribute limit the CSS to this component only */
  .login {
    margin-top: 40px;
  }
  input {
    margin: 10px 0;
    width: 20%;
    padding: 15px;
  }
  button {
    margin-top: 20px;
    width: 10%;
    cursor: pointer;
  }
  p {
    margin-top: 40px;
    font-size: 13px;
  }
  p a {
    text-decoration: underline;
    cursor: pointer;
  }
  </style>