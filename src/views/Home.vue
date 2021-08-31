<template>
<div >
    <section class="section-1 container-fluid">
        <article>
            <h1 class="display-1">Project management has become easier!</h1>
            <p >
                <button id="btn-gst" class="btn btn-info" @click="$router.push('/signup')">Get Started</button>
            </p>
        </article>
            <img src="./../assets/img2.png" alt="" class="img-1 img-fluid">
    </section>

    <section>
        <div class="container text-center animate_animated animated_bounce py-5">
            <h1 class="mb-5">Our Approach</h1>
            <p>Encouraging Agile practices with a focus on <span class="fw-bold">Scrum</span> architecture</p> 
        </div>
    </section>

    <section>
        <div class="container text-center animate_animated animated_bounce py-5" >
            Collaborate, manage projects, and reach new productivity peaks. From high rises to the home office, the way your team works is unique—accomplish it all with Taskup.
            Let the robots do the work—so your team can focus on work that matters. With Trello’s built-in automation, Butler, reduce the number of tedious tasks (and clicks) on your project board by harnessing the power of automation across your entire team.
            </div>
    </section>

    <section>
        <div class="container text-center animate_animated animated_bounce py-5" >
            Powering a productive team means using a powerful tool (and plenty of snacks). From meetings and projects to events and goal setting, Taskup's intuitive features give any team the ability to quickly set up and customize workflows for just about anything.
            Taskup cards are your portal to more organized work—where every single part of your task can be managed, tracked, and shared with teammates. Open any card to uncover an ecosystem of checklists, due dates, attachments, conversations, and more.
            </div>
    </section>
</div>
  
</template>

<script>
// @ is an alias to /src

export default {
  name: 'Home',
  components: {
  }
}
</script>

<!--STYLING-->
<style>
.display-1{
    color:black;
    font-family: Arial, Helvetica, sans-serif;
    font-weight: bolder;
}

.section-1{
    display: flex;
}

.section-1 article{
    padding: 5px;
    margin: 25px 5px 5px 5px;
    max-width: 50%;
    
}

@media screen and (max-width: 770px) {
    .section-1{
    display: inline-block;
}

.section-1 article{
    max-width: unset;
}
}

#btn-gst{
    position: relative;
    width: 36%;
    height: 60px;
    margin: 2em;
    margin-left: 0.5em;
    font-size: 1.2em;
    font-weight: bold;
    font-family: Arial, Helvetica, sans-serif;
}

#btn-gst:active{
    background-color: rgb(250, 203, 203);   
}

.img-1{
    width:50%;
}

@media screen and (max-width: 770px) {
    .img-1{
    width:100%;
}}

</style>
