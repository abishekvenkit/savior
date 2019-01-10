<template lang="html">

  <section class="login">
    <div class="wrapper d-flex align-items-center auth login-full-bg">
      <div class="row w-100">
        <div class="col-lg-6 mx-auto">
          <div class="auth-form-dark text-left p-5">
            <h2>Login</h2>
            <h4 class="font-weight-light">Hello!</h4>
            <form class="pt-5">
              <form>
                <div class="form-group">
                  <label for="exampleInputEmail1">Email</label>
                  <input v-model="email" type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Email">
                  <i class="mdi mdi-account"></i>
                </div>
                <div class="form-group">
                  <label for="exampleInputPassword1">Password</label>
                  <input v-model="password" type="password" class="form-control" id="exampleInputPassword1" placeholder="Password">
                  <i class="mdi mdi-eye"></i>
                </div>
                <div class="mt-5">
                  <a class="btn btn-block btn-warning btn-lg font-weight-medium" @click="login()">Login</a>
                </div>
                <div class="mt-2 text-center" id="error" v-if="error">
                  Your email or password was incorrect. Please try again.
                </div>
              </form>
            </form>
          </div>
        </div>
      </div>
    </div>
  </section>

</template>

<script lang="js">
export default {
  name: 'login',
  data () { return { email: '', password: '', error: false, firebase: require('firebase') }}, 
  methods: {
    login: function() {
      const self = this
      this.firebase.auth().setPersistence(firebase.auth.Auth.Persistence.SESSION).then(() => {

        this.firebase.auth().signInWithEmailAndPassword(this.email, this.password).then((user) => {
        console.log(user)
          this.error = false
          //self.firebase.auth().currentUser.getIdToken(true).then(token => console.log(token))
          
        })
        .catch((error) => {
          this.error = true
          console.log(error)
        })
      }).catch(error => console.log(error))

      
    }
  }
}
</script>
