<script lang="ts">
  import Button from "./Button.svelte";
  const people = ["ak", "dansun", "cjs", "rgong", "jlee", "bwu"];
  export let selected: string = "";
  export let clz = "grid grid-cols-1 2xs:grid-cols-2 xs:grid-cols-3 sm:grid-cols-6 p-2";
</script>

<div class={clz}
>
    {#each people as person}
        <Button
            selected={selected === person}
            selectedClass={"bg-gray-700 ring-gray-700"}
            on:click={() => {
                selected = selected === person ? "" : person;
            }}
        >{person}</Button>
    {/each}
</div>