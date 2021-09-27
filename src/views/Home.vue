<template>
  <div style="min-height:100vh">
    <section class="section-1 container">
      <article class="pt-5">
        <h1 class="display-1">Project <br />management just got easier!</h1>
        <p>
          <button
            id="btn-gst"
            class="btn btn-info"
            @click="$router.push('/signup')"
          >
            Get Started
          </button>
        </p>
      </article>
      <img src="./../assets/img2.png" alt="" class="img-1 img-fluid " style="object-fit:contain;" />
    </section>

    <section class="section-2 container">
      <!-- <div class="container text-center animate_animated animated_bounce py-5">
            <h1 class="mb-5">Our Approach</h1>
            <p>Encouraging Agile practices with a focus on <span class="fw-bold">Scrum</span> architecture</p> 
        </div> -->
      <!-- <article class="transition-2"></article>
      <article class="transition-2"></article>
      <article class="transition-2"></article> -->
    </section>

    <section class="section-3 container">
      <!-- <div class="container text-center animate_animated animated_bounce py-5" >
            Collaborate, manage projects, and reach new productivity peaks. From high rises to the home office, the way your team works is unique—accomplish it all with Taskup.
            Let the robots do the work—so your team can focus on work that matters. With Trello’s built-in automation, Butler, reduce the number of tedious tasks (and clicks) on your project board by harnessing the power of automation across your entire team.
            </div> -->
      <!-- <article class="transition-2"></article>
      <article class="transition-2"></article> -->
    </section>

    <div class="container text-center py-5 comments">
      <div class="col-md-12 m-auto">
        Powering a productive team means using a powerful tool (and plenty of
        snacks). From meetings and projects to events and goal setting, Taskup's
        intuitive features give any team the ability to quickly set up and
        customize workflows for just about anything.
        <br /><br /><br />
        Taskup cards are your portal to more organized work—where every single
        part of your task can be managed, tracked, and shared with teammates.
        Open any card to uncover an ecosystem of checklists, due dates,
        attachments, conversations, and more.
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: "Home",
  components: {},
};
</script>

<!--STYLING-->
<style scoped>
.display-1 {
  color: #2e2d2de0;
  font-family: Cambria, Cochin, Georgia, Times, "Times New Roman", serif;
  font-weight: bolder;
}

.section-1 {
  display: flex;
}

.section-2 {
  display: flex;
}

.section-3 {
  display: flex;
  justify-content: center;
}

.section-2 article {
  background: rgb(224, 198, 132);
  width: 50%;
  margin: 2em;
  margin-top: 50px;
  height: 20em;
  border-radius: 2em;
}

.section-2 article:hover,
.section-2 article:active {
  transform: translateY(-10px);
  box-shadow: 0 0 20px 5px grey;
}

.section-3 article {
  background: rgb(224, 198, 132);
  width: 30%;
  margin: 2em;
  margin-top: 50px;
  height: 20em;
  border-radius: 2em;
}

.section-3 article:hover,
.section-3 article:active {
  transform: translateY(-10px);
  box-shadow: 0 0 20px 5px grey;
}

.section-1 article {
  padding: 5px;
  margin: 25px 5px 5px 5px;
  max-width: 50%;
}

@media screen and (max-width: 770px) {
  .section-1 {
    display: inline-block;
  }
  .section-2 {
    display: inline-block;
  }
  .section-3 {
    display: inline-block;
  }

  .section-1 article {
    max-width: unset;
  }

  .section-2 article {
    width: 95%;
    margin: 4em 0 0 0;
  }

  .section-3 article {
    width: 95%;
    margin: 4em 0 0 0;
  }
}

#btn-gst {
  position: relative;
  width: 36%;
  height: 60px;
  margin: 2em;
  margin-left: 0.5em;
  font-size: 20px;
  font-weight: bold;
  font-family: montserrat;
  border:none;
  border-radius:15px;
  color:white;
  background-color:#24a0ed;
}



.img-1 {
  width: 50%;
}

@media screen and (max-width: 770px) {
  .img-1 {
    width: 100%;
  }

  #btn-gst {
    width: 65%;
  }
}
.comments {
  font-family: montserrat;
  font-size: 20px;
}
</style>
