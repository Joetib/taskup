<template>
  <div class="col-md-3 col-lg-3 col-xl-2 bg-white shadow-sm px-0">
    <div class="container h-100 px-2 pt-5">
      <nav >
        <router-link to="/dashboard/" class="py-2  border border-start-0 border-end-0 border-top-0 d-block  py-3 nav-item nav-link">Dashboard</router-link>
        <router-link to="/tasks/" class="py-2  border border-start-0 border-end-0 border-top-0 d-block  py-3 nav-item nav-link">Tasks</router-link>
        <router-link to="/invites/" class="py-2  border border-start-0 border-end-0 border-top-0 d-block  py-3 nav-item nav-link">Invites</router-link>
        <router-link to="/" class="py-2  border border-start-0 border-end-0 border-top-0 d-block  py-3 nav-item nav-link">Home</router-link>
      </nav>
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style>
</style>