# Fire Extinguisher Inspection App

## Overview

The Fire Extinguisher Inspection App is a desktop application built with Python and Tkinter to streamline and manage fire extinguisher inspections. It provides a straightforward interface to load, inspect, and update the status of fire extinguishers in various locations, allowing inspectors to mark each extinguisher as "Pass" or "Fail" and save their progress. The application also includes helpful visual indicators, such as color-coded statuses, to make it easier to monitor inspection results at a glance.

## Features

- **User-Friendly Interface**: Displays a clean, intuitive GUI for managing fire extinguisher data.
- **Load and Save Functionality**: Users can load a file with fire extinguisher data and save progress during inspections.
- **Monthly Reset**: Provides an option to reset statuses monthly for regular inspections.
- **Search and Filter**: A search bar allows users to quickly locate extinguishers by their properties (such as location or barcode).
- **Toggle Visibility**: Ability to toggle the visibility of Serial Numbers for convenience and reduced visual clutter.

## Data Table Display

The main component of the application is a data table that presents a list of fire extinguishers. The table, implemented using Tkinter's `Treeview` widget, includes the following columns:

- **Location**: The location where the extinguisher is installed.
- **Barcode**: The unique barcode identifier of each extinguisher.
- **Serial Number**: The serial number of each extinguisher (visibility can be toggled).
- **Status**: The current inspection status, which can be marked as "Pass," "Fail," or "Unchecked."

## Status Update and Color Coding

The application allows inspectors to update each extinguisher’s status through "Pass" and "Fail" buttons. Color-coded tags help visually distinguish each status:

- **Pass**: Displays a green background for fire extinguishers marked as "Pass."
- **Fail**: Displays a red background for fire extinguishers marked as "Fail."
- **Unchecked**: Displays a white background for extinguishers that have not been inspected.

This color-coding feature provides an at-a-glance summary of inspection progress, helping inspectors identify issues and prioritize further action.

## Code Highlights

- **UUID Assignment**: Each extinguisher entry is assigned a unique identifier (`UUID`) to track updates more reliably.
- **Selective Status Update**: The app optimizes performance by updating the status of only the selected extinguisher, rather than reloading the entire list.
- **Treeview Scrollbars**: Integrated scrollbars allow for smooth navigation through larger datasets.
  
## Installation

To install and run the app, ensure you have Python installed. Then, clone this repository and install any dependencies listed in `requirements.txt` (such as `pandas`, if needed):

```bash
git clone https://github.com/yourusername/fire-extinguisher-inspection-app.git
cd fire-extinguisher-inspection-app
pip install -r requirements.txt


