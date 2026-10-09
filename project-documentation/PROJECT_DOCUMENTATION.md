# Himalayan Landslide Detection Pipeline

## 1. Executive Summary

The Himalayan area is very likely to have landslides because of hills, weak rocks, heavy rain, earthquakes and changes made by people. Landslides can break buildings stop roads and put people in danger. Using pictures from satellites to find places that might be affected can help speed up checking and make choices for dealing with disasters.

The Himalayan Landslide Detection Pipeline is a system that uses satellites to find and check places that might have landslides. The first plan uses pictures from satellites information about the ground and ways to find changes. The system wants to mix types of clues like how colors look what the ground is like and features from pictures to show signs that need more checking.

The project is still being made. The full system is what is planned; each part and how it works will be written down as it gets done.

## 2. Problem Statement

Checking for landslides in the Himalayas is hard because of hills, not many places to walk quick weather changes and a big area to watch.

Old ways of checking land from the ground take a time and are hard to do right after a big event. Pictures from satellites give a view of the area but it is hard to tell if a change is from a landslide or from plants, snow, shadows, changes in rivers or other natural changes.

There is a need for a way to check satellite pictures think about the ground find changes and show the results in a clear way.

## 3. Project Objectives

The main goals are to:

- Make a way to find changes that could be landslides using satellites.

- Look at pictures before and after an event to see what changed.

- Use information about the height and slope of the ground in the check.

- Try mixing color clues and picture features.

- Make results that show where to look next.

- Make a way to check how good the detection is and how often it makes mistakes.

The system is for checking landslides at first. It is not meant to take the place of checking the land or official decisions about disasters.

## 4. Existing Approaches and Identified Gap

There are ways to use pictures from satellites to find landslides like looking at the pictures by hand checking colors, sorting pictures finding changes and using computer learning to split pictures.

These ways are helpful. They can be affected by clouds, seasons, when the pictures were taken, complex ground and not enough real data.

The big problem is to mix clues without saying everything that changes is a landslide. Thinking about the ground and putting together the clues might help find landslides.

This project tries a way that mixes color changes the ground and new features from pictures in a check. Testing against data will show if it works.

## 5. Proposed Solution

The system has eight steps:

1. Pick the place to check. The landslide event to look at.

2. Get pictures from satellites before and after the event.

3. Use height data. Find things like slope.

4. Look at changes in plants and snow.

5. Use features from a way to see the land.

6. Mix the clues to make a score.

7. Make a map with places that might be landslides.

8. Show the places. Clues through a plan.

These steps show what is planned. How each works and results will be kept separate as the project grows.

## 6. Innovation and Differentiation

The main new idea is to use clues together in one check.

### 6.1 Checking clues

The system uses more than one way to find changes not just one color check.

### 6.2 Checking the ground

Height and slope help understand the changes found. They can help pick places to look. Do not say for sure there is a landslide.

### 6.3 Clear reasons for checking

The score shows which clues helped find a landslide.

### 6.4 Checking the way

The system uses clear steps so others can check the work and make it again.

These are ideas not claims that this is better than ways. Their use will be tested.

## 7. Expected Impact

If it works the system could help:

- Find places that might need checking for landslides.

- Check hard to reach areas fast.

- Pick places to check next.

- Make it clear what the satellites see.

- Make checking the way to help research and disaster checks.

The system is a tool to help with decisions. It needs checks to say for sure if there is a landslide.

## 8. Feasibility and Scope

The first plan uses pictures from satellites and ground data. Sentinel-2 gives pictures for changes while height maps give ground info.

The plan works if there are pictures, right prep, good alignment, good data and enough computer help.

Clouds, snow, shadows, plants and different times when pictures are taken are problems. Using ways and combining clues adds more work.

The first goal is a test system, not a warning system. Checking more and using tools may come later.

## 9. Evaluation Strategy

The system needs data showing where landslides are and where they are not.

Evaluation should look at:

- How often it finds landslides.

- How real landslides it finds.

- A mix of the two above.

- How often it finds things that're not landslides.

- How much the places it finds match ones.

- How fast and how much computer power it uses.

Results will be reported after parts are done. The way data is chosen and checked will be in the plan.

## 10. Limitations and Risk Factors

The main problems include:

- Pictures may not be there or good if there are clouds.

- Plants and snow may look like landslides.

- Ground data may not be good for landslides.

- Different times and weather may cause problems.

- New ways may not work well.

- Not enough or wrong data may not help.

- A check is not a yes or no, for a landslide.

These problems need fixing with steps, checks and being clear.

## 11. Future Scope

-Aligned with India's goal of Aatmanirbhar Bharat
-Align's with india's interest of launching sar satellite and constallations in orbit by 2029. 
-can be used for military and border patrolling use case for inidian army

## 12.. Technical Resources

- [Copernicus Sentinel-2 Mission](https://dataspace.copernicus.eu/explore-data/data-collections/sentinel-data/sentinel-2)

- [Copernicus Data Space Ecosystem](https://dataspace.copernicus.eu/)

- [Google Earth Engine Documentation](https://developers.google.com/earth-engine)

- [NASA Earthdata](https://www.earthdata.nasa.gov/)

- [TerraMind. GitHub Repository](https://github.com/IBM/terramind)

More papers, data and steps will be added as the plan is ready.
