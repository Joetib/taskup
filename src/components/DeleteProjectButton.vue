<template>
<button class="btn btn-danger" @click="delete_project">Delete</button>
</template>

<script>
import axios from 'axios';

export default {
    props : {
        project_id: null
    },
    methods : {
        delete_project(){
            axios.delete(`/project/${this.project_id}/delete/`).then(e=>{
                if (e.data.success){
                    this.$router.push('/dashboard');
                } else {
                    alert("The delete Failed.")
                }
            })
        }
    }

}
</script>
<style>
</style>