# MTL_Map?

## Introduction

I spent a good deal of the winter of 2020 in Toronto missing Montréal. I came home to Montréal just before the pandemic launched itself on Québec, with the end result that I was back in Montréal but I couldn't go to many of the places in Montréal that spelled Montréal for me. To be honest, I'm not even sure some of those places still exist, given how the world has changed since then.

To compensate for the melancholy that comes with being cooped up I've made a tour
of important places in Montréal that users can take to experience different locations
on the city, and hear why they're important to me.

## Vision

My vision for the project involves two separate ways of navigating Montréal:

* A spatial walking tour that allows users to move through Montréal a bit like
someone might move through it while walking.

* An 'emotional' walking tour that would attempt to link spaces not by physical proximity, but by how they are linked in memory. The goal would be a bit to present the tour of Montréal a bit as if one were reading *À la recherche du temps perdu* or
*Mrs. Dalloway*.

I would like the project to have significant visual and textual elements:

* A map showing users where they are in MTL, and what other locations are available (along with some animation showing the trip between the two to make the transitions more felt).

* Illustrations of each location

* Text accompanying each location.

Ultimately I can imagine the tour being deployed as a website after a transition to Rust once I have the framework worked out in Python (the project in part took off because I wanted something to work on in Rust).

## Current status

Currently the project is a Python based text-only tour that allows the user to move between locations along the cardinal directions. The data file is still being written,
but if you really want to try the tour in it's current state let me know and I'll see what I can do.

## Files

Files used in this project include:

* MTL_script.py: Currently this file includes all the functionality for navigating between the different locations, each of which is an instance of the Location class I've written.

* MTL_data.py: While not included in the repo yet, this contains the Location class definition as well as the data to define all the instances of location that are imported by MTL_script.py
