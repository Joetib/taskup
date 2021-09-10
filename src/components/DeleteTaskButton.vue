<template>
<button class="btn btn-danger my-1" @click="delete_project">Delete</button>
</template>

<script>
import axios from 'axios';

export default {
    props : {
        project_id: null,
        task_id:null,
    },
    methods : {
        delete_project(){
            axios.delete(`/project/${this.project_id}/task/${this.task_id}/delete/`).then(e=>{
                if (e.data.success){
                    this.$router.push(`/project/${this.project_id}/`);
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