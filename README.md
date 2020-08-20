# MTL_Map?

## Introduction

I spent a good deal of the winter of 2020 in Toronto missing Montréal. I came home to Montréal just before the pandemic launched itself on Québec, with the end result that I was back in Montréal but I couldn't go to many of the places in Montréal that spelled Montréal for me. To be honest, I'm not even sure some of those places still exist, given how the world has changed since then.

To compensate for the melancholy that comes with being cooped up I've made a tour
of important places in Montréal that users can take to experience different locations
on the city, and hear why they're important to me.

## Vision

My vision for the project involves three separate ways of navigating Montréal:


* A spatial walking tour that allows users to move through Montréal a bit like someone might move through it while walking. The user can choose to move north, south, east, west, to the closest location, or to a random location.

* An temporal walking tour that allows users to move forward or backward in time, as well as visits to random locations from each of the four seasons.

* An 'emotional' walking tour that doesn't link spaces by physical or temporal proximity, but by how they are linked in memory. The goal would be a bit to present the tour of Montréal a bit as if one were reading *À la recherche du temps perdu* or *Mrs. Dalloway*. The current implementation of this leads the user to the memory with the highest cosine similarity to the current memory (unless that was the preceding memory).

Ultimately I would like the project to have significant visual and textual elements:

* A map showing users where they are in MTL, and what other locations are available (along with some animation showing the trip between the two to make the transitions more felt).

* Illustrations of each location

* Text accompanying each location.

I can imagine the tour being deployed as a website after the ongoing transition to Rust is complete (the project in part took off because I wanted something to work on in Rust).

## Current status

The spatial and temporal walking tours are complete, while the emotional walking tour has basic functionality.

## Files

Files used in this project include:

* MTL_script.py: Currently this file includes all the functionality for navigating between the different locations, each of which is an instance of the Location class I've written.

* MTL_Classes.py: Contains the Location class definition called by MTL_data.py.

* MTL_data.py: Includes dummy memories to demonstrate functionality. In the actual distribution there would be more memories, and much more extensive descriptions of each.

* MTL_py2rust.py: A script that uses regex to convert Python Location objects into Rust Location structs. This file isn't strictly necessary for the functionality of either the Python or the Rust versions of this project, but provides an easy way to convert the locations written in Python into ones that can be used for the Rust project (this reflects how initial development was done in Python with conversion to Rust once functionality was established).
