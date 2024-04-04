<script>
export default {
  data () {
    return {
      loading: false,
      showResults: false,
      results: [
      {
          site_name: "ESPN",
          site_link: "https://www.espn.com",
          headline: "Lionel Messi rumored to be considering transfer to PSG",
          description: "Reports suggest that Lionel Messi is in talks with Paris Saint-Germain (PSG) for a potential transfer.",
        },
        {
          site_name: "Goal",
          site_link: "https://www.goal.com",
          headline: "Breaking: Messi to leave Barcelona for Manchester City",
          description: "In a shocking turn of events, Lionel Messi has announced his decision to leave Barcelona and join Manchester City.",
        },
        {
          site_name: "BBC Sport",
          site_link: "https://www.bbc.com/sport",
          headline: "Messi's future uncertain as contract talks with Barcelona stall",
          description: "Negotiations between Lionel Messi and Barcelona have hit a roadblock, raising doubts about the star player's future at the club.",
        },
        {
          site_name: "Sky Sports",
          site_link: "https://www.skysports.com/football",
          headline: "Messi linked with move to MLS",
          description: "Speculation is rife that Lionel Messi could be heading to Major League Soccer (MLS) in the United States.",
        },
        {
          site_name: "ESPN",
          site_link: "https://www.espn.com",
          headline: "Lionel Messi rumored to be considering transfer to PSG",
          description: "Reports suggest that Lionel Messi is in talks with Paris Saint-Germain (PSG) for a potential transfer.",
        },
        {
          site_name: "Goal",
          site_link: "https://www.goal.com",
          headline: "Breaking: Messi to leave Barcelona for Manchester City",
          description: "In a shocking turn of events, Lionel Messi has announced his decision to leave Barcelona and join Manchester City.",
        },
        {
          site_name: "BBC Sport",
          site_link: "https://www.bbc.com/sport",
          headline: "Messi's future uncertain as contract talks with Barcelona stall",
          description: "Negotiations between Lionel Messi and Barcelona have hit a roadblock, raising doubts about the star player's future at the club.",
        },
        {
          site_name: "Sky Sports",
          site_link: "https://www.skysports.com/football",
          headline: "Messi linked with move to MLS",
          description: "Speculation is rife that Lionel Messi could be heading to Major League Soccer (MLS) in the United States.",
        }
      ]
    }
  },

  methods: {
    getResults() {
      this.loading = true

      setTimeout(() => {
        this.showResults = true
        this.loading = false
      }, 300)
    }
  }
}
</script>

<template>
  <div class="content">
    <h1>Swift Search</h1>
    <form>
      <input type="text" class="search-box"/>
      <button class="submit" type="submit" @click.prevent="getResults()">Go!</button>
    </form>
    <div class="loading" v-if="loading">Loading...</div>
    <div class="toolbar" v-if="showResults">
      <button>Sort by Relevance</button>
      <button>Sort by Date</button>
      <button>Filter by Date</button>
    </div>
    <div class="search-results" v-if="showResults">
        <div v-for="result in results" :key="result.id" class="result">
            <div>{{ result.site_name }}</div>
            <a href="result.site_link" target="_blank">{{  result.site_link }}</a>
            <div class="headline">{{  result.headline }}</div>
            <div>{{  result.description }}</div>
        </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}

.content {
  background-color: white;
  color: black;
  text-align: center;
  display: flex;
  flex-direction: column;
}

.search-box {
  padding: 1rem;
  border-radius: 1rem;
  width: 25rem;
  margin-right: 1rem;
}

.submit {
  cursor: pointer;
  background-color: #0d6efd;
  border: none;
  border-radius: 50%;
  color: white;
  height: 3rem;
  width: 3rem;
}

.search-results {
  margin: 1rem auto;
}

.result {
  cursor: pointer;
  display: flex;
  flex-direction: column;
  margin-bottom: 2rem;
  text-align: left;

  .headline {
    font-size: 1.5rem;
  }
}

.toolbar {
  margin: 1rem 0;

  button {
    cursor: pointer;
    margin-right: 1rem;
  }
}
</style>
