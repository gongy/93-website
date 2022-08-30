<script lang="ts">
  import clsx from "clsx";
  import Expenses from "./Expenses.svelte";
  import Laundry from "./Laundry.svelte";
  import Button from "./Button.svelte";
  import {
    BoxIcon,
    CreditCardIcon,
    LogInIcon,
    SpeakerIcon,
    UserIcon,
  } from "svelte-feather-icons";
  import jwt_decode from "jwt-decode";

  const options = [
    { name: "Laundry", icon: SpeakerIcon },
    { name: "Expenses", icon: CreditCardIcon },
    { name: "Guests", icon: UserIcon },
    { name: "Packages", icon: BoxIcon },
  ];

  let selected: string = "Laundry";
  let card: any;

  let credential: any = undefined;
  let user: any;

  (window as any).handleCredentialResponse = (response: any) => {
    user = jwt_decode(response.credential);
    console.log("ID: " + user.sub);
    console.log('Full Name: ' + user.name);
    console.log('Given Name: ' + user.given_name);
    console.log('Family Name: ' + user.family_name);
    console.log("Image URL: " + user.picture);
    console.log("Email: " + user.email);
    credential = response.credential;
  }
</script>

<svelte:head>
  <script src="https://accounts.google.com/gsi/client" async defer></script>
</svelte:head>

<main>
  <h1 class="flex justify-center pt-10 pb-8">
    {#if user}
      <img class="invisible rounded-full w-8 h-8 my-auto" src={user.picture} alt={user.name}/>
    {/if}
    <div class="text-center mx-auto text-zinc-100 text-3xl font-light">
      93 Leonard
    </div>
    {#if user}
      <img class="rounded-full w-8 h-8 my-auto" src={user.picture} alt={user.name}/>
    {/if}
  </h1>

  <div class="grid grid-cols-1 2xs:grid-cols-2 sm:grid-cols-4 pb-3">
    {#each options as option (option)}
      <Button
        selectedClass="bg-gray-700 ring-gray-700"
        selected={selected === option.name}
        on:click={() => {
          selected = option.name;
        }}
      >
        <div class="flex align-center justify-center">
          <svelte:component
            this={option.icon}
            bind:this={card}
            class="flex-shrink-0 w-5 h-5 mx-1 mt-0.5"
          />
          <div class="mx-1">{option.name}</div>
        </div>
      </Button>
    {/each}
  </div>

  {#if !user}
    <div class="flex justify-center pt-5">
      <div id="g_id_onload"
        data-client_id="971159492117-cc6jhib74lf8egu0cm67v73jr20k4vvt.apps.googleusercontent.com"
        data-callback="handleCredentialResponse"
        data-auto_prompt="false">
      </div>
      <div class="g_id_signin"
        data-type="standard"
        data-size="large"
        data-theme="filled_black"
        data-text="signin"
        data-shape="rectangular"
        data-logo_alignment="left">
        hello
      </div>
    </div>
  {:else}
    <div>
      {#if selected == "Expenses"}
        <Expenses/>
      {:else if selected == "Laundry"}
        <Laundry/>
      {/if}
    </div>
  {/if}
</main>
