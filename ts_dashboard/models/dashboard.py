# -*- coding: utf-8 -*-
import json
import logging
import datetime
from odoo import api, fields, models,_
from odoo.tools.safe_eval import safe_eval
from datetime import timedelta
from dateutil import relativedelta

logger = logging.getLogger(__name__)
CHART_COLORS = [('brewer.YlGn4', 'brewer.YlGn4'), ('brewer.YlGn5', 'brewer.YlGn5'), ('brewer.YlGn6', 'brewer.YlGn6'),
                ('brewer.YlGn7', 'brewer.YlGn7'), ('brewer.YlGn8', 'brewer.YlGn8'), ('brewer.YlGn9', 'brewer.YlGn9'),
                ('brewer.YlGnBu3', 'brewer.YlGnBu3'), ('brewer.YlGnBu4', 'brewer.YlGnBu4'),
                ('brewer.YlGnBu5', 'brewer.YlGnBu5'), ('brewer.YlGnBu6', 'brewer.YlGnBu6'),
                ('brewer.YlGnBu7', 'brewer.YlGnBu7'), ('brewer.YlGnBu8', 'brewer.YlGnBu8'),
                ('brewer.YlGnBu9', 'brewer.YlGnBu9'), ('brewer.GnBu3', 'brewer.GnBu3'),
                ('brewer.GnBu4', 'brewer.GnBu4'), ('brewer.GnBu5', 'brewer.GnBu5'), ('brewer.GnBu6', 'brewer.GnBu6'),
                ('brewer.GnBu7', 'brewer.GnBu7'), ('brewer.GnBu8', 'brewer.GnBu8'), ('brewer.GnBu9', 'brewer.GnBu9'),
                ('brewer.BuGn3', 'brewer.BuGn3'), ('brewer.BuGn4', 'brewer.BuGn4'), ('brewer.BuGn5', 'brewer.BuGn5'),
                ('brewer.BuGn6', 'brewer.BuGn6'), ('brewer.BuGn7', 'brewer.BuGn7'), ('brewer.BuGn8', 'brewer.BuGn8'),
                ('brewer.BuGn9', 'brewer.BuGn9'), ('brewer.PuBuGn3', 'brewer.PuBuGn3'),
                ('brewer.PuBuGn4', 'brewer.PuBuGn4'), ('brewer.PuBuGn5', 'brewer.PuBuGn5'),
                ('brewer.PuBuGn6', 'brewer.PuBuGn6'), ('brewer.PuBuGn7', 'brewer.PuBuGn7'),
                ('brewer.PuBuGn8', 'brewer.PuBuGn8'), ('brewer.PuBuGn9', 'brewer.PuBuGn9'),
                ('brewer.PuBu3', 'brewer.PuBu3'), ('brewer.PuBu4', 'brewer.PuBu4'), ('brewer.PuBu5', 'brewer.PuBu5'),
                ('brewer.PuBu6', 'brewer.PuBu6'), ('brewer.PuBu7', 'brewer.PuBu7'), ('brewer.PuBu8', 'brewer.PuBu8'),
                ('brewer.PuBu9', 'brewer.PuBu9'), ('brewer.BuPu3', 'brewer.BuPu3'), ('brewer.BuPu4', 'brewer.BuPu4'),
                ('brewer.BuPu5', 'brewer.BuPu5'), ('brewer.BuPu6', 'brewer.BuPu6'), ('brewer.BuPu7', 'brewer.BuPu7'),
                ('brewer.BuPu8', 'brewer.BuPu8'), ('brewer.BuPu9', 'brewer.BuPu9'), ('brewer.RdPu3', 'brewer.RdPu3'),
                ('brewer.RdPu4', 'brewer.RdPu4'), ('brewer.RdPu5', 'brewer.RdPu5'), ('brewer.RdPu6', 'brewer.RdPu6'),
                ('brewer.RdPu7', 'brewer.RdPu7'), ('brewer.RdPu8', 'brewer.RdPu8'), ('brewer.RdPu9', 'brewer.RdPu9'),
                ('brewer.PuRd3', 'brewer.PuRd3'), ('brewer.PuRd4', 'brewer.PuRd4'), ('brewer.PuRd5', 'brewer.PuRd5'),
                ('brewer.PuRd6', 'brewer.PuRd6'), ('brewer.PuRd7', 'brewer.PuRd7'), ('brewer.PuRd8', 'brewer.PuRd8'),
                ('brewer.PuRd9', 'brewer.PuRd9'), ('brewer.OrRd3', 'brewer.OrRd3'), ('brewer.OrRd4', 'brewer.OrRd4'),
                ('brewer.OrRd5', 'brewer.OrRd5'), ('brewer.OrRd6', 'brewer.OrRd6'), ('brewer.OrRd7', 'brewer.OrRd7'),
                ('brewer.OrRd8', 'brewer.OrRd8'), ('brewer.OrRd9', 'brewer.OrRd9'),
                ('brewer.YlOrRd3', 'brewer.YlOrRd3'), ('brewer.YlOrRd4', 'brewer.YlOrRd4'),
                ('brewer.YlOrRd5', 'brewer.YlOrRd5'), ('brewer.YlOrRd6', 'brewer.YlOrRd6'),
                ('brewer.YlOrRd7', 'brewer.YlOrRd7'), ('brewer.YlOrRd8', 'brewer.YlOrRd8'),
                ('brewer.YlOrRd9', 'brewer.YlOrRd9'), ('brewer.YlOrBr3', 'brewer.YlOrBr3'),
                ('brewer.YlOrBr4', 'brewer.YlOrBr4'), ('brewer.YlOrBr5', 'brewer.YlOrBr5'),
                ('brewer.YlOrBr6', 'brewer.YlOrBr6'), ('brewer.YlOrBr7', 'brewer.YlOrBr7'),
                ('brewer.YlOrBr8', 'brewer.YlOrBr8'), ('brewer.YlOrBr9', 'brewer.YlOrBr9'),
                ('brewer.Purples3', 'brewer.Purples3'), ('brewer.Purples4', 'brewer.Purples4'),
                ('brewer.Purples5', 'brewer.Purples5'), ('brewer.Purples6', 'brewer.Purples6'),
                ('brewer.Purples7', 'brewer.Purples7'), ('brewer.Purples8', 'brewer.Purples8'),
                ('brewer.Purples9', 'brewer.Purples9'), ('brewer.Blues3', 'brewer.Blues3'),
                ('brewer.Blues4', 'brewer.Blues4'), ('brewer.Blues5', 'brewer.Blues5'),
                ('brewer.Blues6', 'brewer.Blues6'), ('brewer.Blues7', 'brewer.Blues7'),
                ('brewer.Blues8', 'brewer.Blues8'), ('brewer.Blues9', 'brewer.Blues9'),
                ('brewer.Greens3', 'brewer.Greens3'), ('brewer.Greens4', 'brewer.Greens4'),
                ('brewer.Greens5', 'brewer.Greens5'), ('brewer.Greens6', 'brewer.Greens6'),
                ('brewer.Greens7', 'brewer.Greens7'), ('brewer.Greens8', 'brewer.Greens8'),
                ('brewer.Greens9', 'brewer.Greens9'), ('brewer.Oranges3', 'brewer.Oranges3'),
                ('brewer.Oranges4', 'brewer.Oranges4'), ('brewer.Oranges5', 'brewer.Oranges5'),
                ('brewer.Oranges6', 'brewer.Oranges6'), ('brewer.Oranges7', 'brewer.Oranges7'),
                ('brewer.Oranges8', 'brewer.Oranges8'), ('brewer.Oranges9', 'brewer.Oranges9'),
                ('brewer.Reds3', 'brewer.Reds3'), ('brewer.Reds4', 'brewer.Reds4'), ('brewer.Reds5', 'brewer.Reds5'),
                ('brewer.Reds6', 'brewer.Reds6'), ('brewer.Reds7', 'brewer.Reds7'), ('brewer.Reds8', 'brewer.Reds8'),
                ('brewer.Reds9', 'brewer.Reds9'), ('brewer.Greys3', 'brewer.Greys3'),
                ('brewer.Greys4', 'brewer.Greys4'), ('brewer.Greys5', 'brewer.Greys5'),
                ('brewer.Greys6', 'brewer.Greys6'), ('brewer.Greys7', 'brewer.Greys7'),
                ('brewer.Greys8', 'brewer.Greys8'), ('brewer.Greys9', 'brewer.Greys9'),
                ('brewer.PuOr3', 'brewer.PuOr3'), ('brewer.PuOr4', 'brewer.PuOr4'), ('brewer.PuOr5', 'brewer.PuOr5'),
                ('brewer.PuOr6', 'brewer.PuOr6'), ('brewer.PuOr7', 'brewer.PuOr7'), ('brewer.PuOr8', 'brewer.PuOr8'),
                ('brewer.PuOr9', 'brewer.PuOr9'), ('brewer.PuOr10', 'brewer.PuOr10'),
                ('brewer.PuOr11', 'brewer.PuOr11'), ('brewer.BrBG3', 'brewer.BrBG3'), ('brewer.BrBG4', 'brewer.BrBG4'),
                ('brewer.BrBG5', 'brewer.BrBG5'), ('brewer.BrBG6', 'brewer.BrBG6'), ('brewer.BrBG7', 'brewer.BrBG7'),
                ('brewer.BrBG8', 'brewer.BrBG8'), ('brewer.BrBG9', 'brewer.BrBG9'), ('brewer.BrBG10', 'brewer.BrBG10'),
                ('brewer.BrBG11', 'brewer.BrBG11'), ('brewer.PRGn3', 'brewer.PRGn3'), ('brewer.PRGn4', 'brewer.PRGn4'),
                ('brewer.PRGn5', 'brewer.PRGn5'), ('brewer.PRGn6', 'brewer.PRGn6'), ('brewer.PRGn7', 'brewer.PRGn7'),
                ('brewer.PRGn8', 'brewer.PRGn8'), ('brewer.PRGn9', 'brewer.PRGn9'), ('brewer.PRGn10', 'brewer.PRGn10'),
                ('brewer.PRGn11', 'brewer.PRGn11'), ('brewer.PiYG3', 'brewer.PiYG3'), ('brewer.PiYG4', 'brewer.PiYG4'),
                ('brewer.PiYG5', 'brewer.PiYG5'), ('brewer.PiYG6', 'brewer.PiYG6'), ('brewer.PiYG7', 'brewer.PiYG7'),
                ('brewer.PiYG8', 'brewer.PiYG8'), ('brewer.PiYG9', 'brewer.PiYG9'), ('brewer.PiYG10', 'brewer.PiYG10'),
                ('brewer.PiYG11', 'brewer.PiYG11'), ('brewer.RdBu3', 'brewer.RdBu3'), ('brewer.RdBu4', 'brewer.RdBu4'),
                ('brewer.RdBu5', 'brewer.RdBu5'),
                ('brewer.RdBu6', 'brewer.RdBu6'),
                ('brewer.RdBu7', 'brewer.RdBu7'),
                ('brewer.RdBu8', 'brewer.RdBu8'),
                ('brewer.RdBu9', 'brewer.RdBu9'),
                ('brewer.RdBu10', 'brewer.RdBu10'),
                ('brewer.RdBu11', 'brewer.RdBu11'),
                ('brewer.RdGy3', 'brewer.RdGy3'),
                ('brewer.RdGy4', 'brewer.RdGy4'),
                ('brewer.RdGy5', 'brewer.RdGy5'),
                ('brewer.RdGy6', 'brewer.RdGy6'),
                ('brewer.RdGy7', 'brewer.RdGy7'),
                ('brewer.RdGy8', 'brewer.RdGy8'),
                ('brewer.RdGy9', 'brewer.RdGy9'),
                ('brewer.RdGy10', 'brewer.RdGy10'),
                ('brewer.RdGy11', 'brewer.RdGy11'),
                ('brewer.RdYlBu3', 'brewer.RdYlBu3'),
                ('brewer.RdYlBu4', 'brewer.RdYlBu4'),
                ('brewer.RdYlBu5', 'brewer.RdYlBu5'),
                ('brewer.RdYlBu6', 'brewer.RdYlBu6'),
                ('brewer.RdYlBu7', 'brewer.RdYlBu7'),
                ('brewer.RdYlBu8', 'brewer.RdYlBu8'),
                ('brewer.RdYlBu9', 'brewer.RdYlBu9'),
                ('brewer.RdYlBu10', 'brewer.RdYlBu10'),
                ('brewer.RdYlBu11', 'brewer.RdYlBu11'),
                ('brewer.Spectral3', 'brewer.Spectral3'),
                ('brewer.Spectral4', 'brewer.Spectral4'),
                ('brewer.Spectral5', 'brewer.Spectral5'),
                ('brewer.Spectral6', 'brewer.Spectral6'),
                ('brewer.Spectral7', 'brewer.Spectral7'),
                ('brewer.Spectral8', 'brewer.Spectral8'),
                ('brewer.Spectral9', 'brewer.Spectral9'),
                ('brewer.Spectral10', 'brewer.Spectral10'),
                ('brewer.Spectral11', 'brewer.Spectral11'),
                ('brewer.RdYlGn3', 'brewer.RdYlGn3'),
                ('brewer.RdYlGn4', 'brewer.RdYlGn4'),
                ('brewer.RdYlGn5', 'brewer.RdYlGn5'),
                ('brewer.RdYlGn6', 'brewer.RdYlGn6'),
                ('brewer.RdYlGn7', 'brewer.RdYlGn7'),
                ('brewer.RdYlGn8', 'brewer.RdYlGn8'),
                ('brewer.RdYlGn9', 'brewer.RdYlGn9'),
                ('brewer.RdYlGn10', 'brewer.RdYlGn10'),
                ('brewer.RdYlGn11', 'brewer.RdYlGn11'),
                ('brewer.Accent3', 'brewer.Accent3'),
                ('brewer.Accent4', 'brewer.Accent4'),
                ('brewer.Accent5', 'brewer.Accent5'),
                ('brewer.Accent6', 'brewer.Accent6'),
                ('brewer.Accent7', 'brewer.Accent7'),
                ('brewer.Accent8', 'brewer.Accent8'),
                ('brewer.DarkTwo3', 'brewer.DarkTwo3'),
                ('brewer.DarkTwo4', 'brewer.DarkTwo4'),
                ('brewer.DarkTwo5', 'brewer.DarkTwo5'),
                ('brewer.DarkTwo6', 'brewer.DarkTwo6'),
                ('brewer.DarkTwo7', 'brewer.DarkTwo7'),
                ('brewer.DarkTwo8', 'brewer.DarkTwo8'),
                ('brewer.Paired3', 'brewer.Paired3'),
                ('brewer.Paired4', 'brewer.Paired4'),
                ('brewer.Paired5', 'brewer.Paired5'),
                ('brewer.Paired6', 'brewer.Paired6'),
                ('brewer.Paired7', 'brewer.Paired7'),
                ('brewer.Paired8', 'brewer.Paired8'),
                ('brewer.Paired9', 'brewer.Paired9'),
                ('brewer.Paired10', 'brewer.Paired10'),
                ('brewer.Paired11', 'brewer.Paired11'),
                ('brewer.Paired12', 'brewer.Paired12'),
                ('brewer.PastelOne3', 'brewer.PastelOne3'),
                ('brewer.PastelOne4', 'brewer.PastelOne4'),
                ('brewer.PastelOne5', 'brewer.PastelOne5'),
                ('brewer.PastelOne6', 'brewer.PastelOne6'),
                ('brewer.PastelOne7', 'brewer.PastelOne7'),
                ('brewer.PastelOne8', 'brewer.PastelOne8'),
                ('brewer.PastelOne9', 'brewer.PastelOne9'),
                ('brewer.PastelTwo3', 'brewer.PastelTwo3'),
                ('brewer.PastelTwo4', 'brewer.PastelTwo4'),
                ('brewer.PastelTwo5', 'brewer.PastelTwo5'),
                ('brewer.PastelTwo6', 'brewer.PastelTwo6'),
                ('brewer.PastelTwo7', 'brewer.PastelTwo7'),
                ('brewer.PastelTwo8', 'brewer.PastelTwo8'),
                ('brewer.SetOne3', 'brewer.SetOne3'),
                ('brewer.SetOne4', 'brewer.SetOne4'),
                ('brewer.SetOne5', 'brewer.SetOne5'),
                ('brewer.SetOne6', 'brewer.SetOne6'),
                ('brewer.SetOne7', 'brewer.SetOne7'),
                ('brewer.SetOne8', 'brewer.SetOne8'),
                ('brewer.SetOne9', 'brewer.SetOne9'),
                ('brewer.SetTwo3', 'brewer.SetTwo3'),
                ('brewer.SetTwo4', 'brewer.SetTwo4'),
                ('brewer.SetTwo5', 'brewer.SetTwo5'),
                ('brewer.SetTwo6', 'brewer.SetTwo6'),
                ('brewer.SetTwo7', 'brewer.SetTwo7'),
                ('brewer.SetTwo8', 'brewer.SetTwo8'),
                ('brewer.SetThree3', 'brewer.SetThree3'),
                ('brewer.SetThree4', 'brewer.SetThree4'),
                ('brewer.SetThree5', 'brewer.SetThree5'),
                ('brewer.SetThree6', 'brewer.SetThree6'),
                ('brewer.SetThree7', 'brewer.SetThree7'),
                ('brewer.SetThree8', 'brewer.SetThree8'),
                ('brewer.SetThree9', 'brewer.SetThree9'),
                ('brewer.SetThree10', 'brewer.SetThree10'),
                ('brewer.SetThree11', 'brewer.SetThree11'),
                ('brewer.SetThree12', 'brewer.SetThree12'),
                ('office.Adjacency6', 'office.Adjacency6'),
                ('office.Advantage6', 'office.Advantage6'),
                ('office.Angles6', 'office.Angles6'),
                ('office.Apex6', 'office.Apex6'),
                ('office.Apothecary6', 'office.Apothecary6'),
                ('office.Aspect6', 'office.Aspect6'),
                ('office.Atlas6', 'office.Atlas6'),
                ('office.Austin6', 'office.Austin6'),
                ('office.Badge6', 'office.Badge6'),
                ('office.Banded6', 'office.Banded6'),
                ('office.Basis6', 'office.Basis6'),
                ('office.Berlin6', 'office.Berlin6'),
                ('office.BlackTie6', 'office.BlackTie6'),
                ('office.Blue6', 'office.Blue6'),
                ('office.BlueGreen6', 'office.BlueGreen6'),
                ('office.BlueII6', 'office.BlueII6'),
                ('office.BlueRed6', 'office.BlueRed6'),
                ('office.BlueWarm6', 'office.BlueWarm6'),
                ('office.Breeze6', 'office.Breeze6'),
                ('office.Capital6', 'office.Capital6'),
                ('office.Celestial6', 'office.Celestial6'),
                ('office.Circuit6', 'office.Circuit6'),
                ('office.Civic6', 'office.Civic6'),
                ('office.Clarity6', 'office.Clarity6'),
                ('office.Codex6', 'office.Codex6'),
                ('office.Composite6', 'office.Composite6'),
                ('office.Concourse6', 'office.Concourse6'),
                ('office.Couture6', 'office.Couture6'),
                ('office.Crop6', 'office.Crop6'),
                ('office.Damask6', 'office.Damask6'),
                ('office.Depth6', 'office.Depth6'),
                ('office.Dividend6', 'office.Dividend6'),
                ('office.Droplet6', 'office.Droplet6'),
                ('office.Elemental6', 'office.Elemental6'),
                ('office.Equity6', 'office.Equity6'),
                ('office.Essential6', 'office.Essential6'),
                ('office.Excel16', 'office.Excel16'),
                ('office.Executive6', 'office.Executive6'),
                ('office.Exhibit6', 'office.Exhibit6'),
                ('office.Expo6', 'office.Expo6'),
                ('office.Facet6', 'office.Facet6'),
                ('office.Feathered6', 'office.Feathered6'),
                ('office.Flow6', 'office.Flow6'),
                ('office.Focus6', 'office.Focus6'),
                ('office.Folio6', 'office.Folio6'),
                ('office.Formal6', 'office.Formal6'),
                ('office.Forte6', 'office.Forte6'),
                ('office.Foundry6', 'office.Foundry6'),
                ('office.Frame6', 'office.Frame6'),
                ('office.Gallery6', 'office.Gallery6'),
                ('office.Genesis6', 'office.Genesis6'),
                ('office.Grayscale6', 'office.Grayscale6'),
                ('office.Green6', 'office.Green6'),
                ('office.GreenYellow6', 'office.GreenYellow6'),
                ('office.Grid6', 'office.Grid6'),
                ('office.Habitat6', 'office.Habitat6'),
                ('office.Hardcover6', 'office.Hardcover6'),
                ('office.Headlines6', 'office.Headlines6'),
                ('office.Horizon6', 'office.Horizon6'),
                ('office.Infusion6', 'office.Infusion6'),
                ('office.Inkwell6', 'office.Inkwell6'),
                ('office.Inspiration6', 'office.Inspiration6'),
                ('office.Integral6', 'office.Integral6'),
                ('office.Ion6', 'office.Ion6'),
                ('office.IonBoardroom6', 'office.IonBoardroom6'),
                ('office.Kilter6', 'office.Kilter6'),
                ('office.Madison6', 'office.Madison6'),
                ('office.MainEvent6', 'office.MainEvent6'),
                ('office.Marquee6', 'office.Marquee6'),
                ('office.Median6', 'office.Median6'),
                ('office.Mesh6', 'office.Mesh6'),
                ('office.Metail6', 'office.Metail6'),
                ('office.Metro6', 'office.Metro6'),
                ('office.Metropolitan6', 'office.Metropolitan6'),
                ('office.Module6', 'office.Module6'),
                ('office.NewsPrint6', 'office.NewsPrint6'),
                ('office.Office6', 'office.Office6'),
                ('office.OfficeClassic6', 'office.OfficeClassic6'),
                ('office.Opulent6', 'office.Opulent6'),
                ('office.Orange6', 'office.Orange6'),
                ('office.OrangeRed6', 'office.OrangeRed6'),
                ('office.Orbit6', 'office.Orbit6'),
                ('office.Organic6', 'office.Organic6'),
                ('office.Oriel6', 'office.Oriel6'),
                ('office.Origin6', 'office.Origin6'),
                ('office.Paper6', 'office.Paper6'),
                ('office.Parallax6', 'office.Parallax6'),
                ('office.Parcel6', 'office.Parcel6'),
                ('office.Perception6', 'office.Perception6'),
                ('office.Perspective6', 'office.Perspective6'),
                ('office.Pixel6', 'office.Pixel6'),
                ('office.Plaza6', 'office.Plaza6'),
                ('office.Precedent6', 'office.Precedent6'),
                ('office.Pushpin6', 'office.Pushpin6'),
                ('office.Quotable6', 'office.Quotable6'),
                ('office.Red6', 'office.Red6'),
                ('office.RedOrange6', 'office.RedOrange6'),
                ('office.RedViolet6', 'office.RedViolet6'),
                ('office.Retrospect6', 'office.Retrospect6'),
                ('office.Revolution6', 'office.Revolution6'),
                ('office.Saddle6', 'office.Saddle6'),
                ('office.Savon6', 'office.Savon6'),
                ('office.Sketchbook6', 'office.Sketchbook6'),
                ('office.Sky6', 'office.Sky6'),
                ('office.Slate6', 'office.Slate6'),
                ('office.Slice6', 'office.Slice6'),
                ('office.Slipstream6', 'office.Slipstream6'),
                ('office.SOHO6', 'office.SOHO6'),
                ('office.Solstice6', 'office.Solstice6'),
                ('office.Spectrum6', 'office.Spectrum6'),
                ('office.Story6', 'office.Story6'),
                ('office.Studio6', 'office.Studio6'),
                ('office.Summer6', 'office.Summer6'),
                ('office.Technic6', 'office.Technic6'),
                ('office.Thatch6', 'office.Thatch6'),
                ('office.Tradition6', 'office.Tradition6'),
                ('office.Travelogue6', 'office.Travelogue6'),
                ('office.Trek6', 'office.Trek6'),
                ('office.Twilight6', 'office.Twilight6'),
                ('office.Urban6', 'office.Urban6'),
                ('office.UrbanPop6', 'office.UrbanPop6'),
                ('office.VaporTrail6', 'office.VaporTrail6'),
                ('office.Venture6', 'office.Venture6'),
                ('office.Verve6', 'office.Verve6'),
                ('office.View6', 'office.View6'),
                ('office.Violet6', 'office.Violet6'),
                ('office.VioletII6', 'office.VioletII6'),
                ('office.Waveform6', 'office.Waveform6'),
                ('office.Wisp6', 'office.Wisp6'),
                ('office.WoodType6', 'office.WoodType6'),
                ('office.Yellow6', 'office.Yellow6'),
                ('office.YellowOrange6', 'office.YellowOrange6'),
                ('tableau.Tableau10', 'tableau.Tableau10'),
                ('tableau.Tableau20', 'tableau.Tableau20'),
                ('tableau.ColorBlind10', 'tableau.ColorBlind10'),
                ('tableau.SeattleGrays5', 'tableau.SeattleGrays5'),
                ('tableau.Traffic9', 'tableau.Traffic9'),
                ('tableau.MillerStone11', 'tableau.MillerStone11'),
                ('tableau.SuperfishelStone10', 'tableau.SuperfishelStone10'),
                ('tableau.NurielStone9', 'tableau.NurielStone9'),
                ('tableau.JewelBright9', 'tableau.JewelBright9'),
                ('tableau.Summer8', 'tableau.Summer8'),
                ('tableau.Winter10', 'tableau.Winter10'),
                ('tableau.GreenOrangeTeal12', 'tableau.GreenOrangeTeal12'),
                ('tableau.RedBlueBrown12', 'tableau.RedBlueBrown12'),
                ('tableau.PurplePinkGray12', 'tableau.PurplePinkGray12'),
                ('tableau.HueCircle19', 'tableau.HueCircle19'),
                ('tableau.OrangeBlue7', 'tableau.OrangeBlue7'),
                ('tableau.RedGreen7', 'tableau.RedGreen7'),
                ('tableau.GreenBlue7', 'tableau.GreenBlue7'),
                ('tableau.RedBlue7', 'tableau.RedBlue7'),
                ('tableau.RedBlack7', 'tableau.RedBlack7'),
                ('tableau.GoldPurple7', 'tableau.GoldPurple7'),
                ('tableau.RedGreenGold7', 'tableau.RedGreenGold7'),
                ('tableau.SunsetSunrise7', 'tableau.SunsetSunrise7'),
                ('tableau.OrangeBlueWhite7', 'tableau.OrangeBlueWhite7'),
                ('tableau.RedGreenWhite7', 'tableau.RedGreenWhite7'),
                ('tableau.GreenBlueWhite7', 'tableau.GreenBlueWhite7'),
                ('tableau.RedBlueWhite7', 'tableau.RedBlueWhite7'),
                ('tableau.RedBlackWhite7', 'tableau.RedBlackWhite7'),
                ('tableau.OrangeBlueLight7', 'tableau.OrangeBlueLight7'),
                ('tableau.Temperature7', 'tableau.Temperature7'),
                ('tableau.BlueGreen7', 'tableau.BlueGreen7'),
                ('tableau.BlueLight7', 'tableau.BlueLight7'),
                ('tableau.OrangeLight7', 'tableau.OrangeLight7'),
                ('tableau.Blue20', 'tableau.Blue20'),
                ('tableau.Orange20', 'tableau.Orange20'),
                ('tableau.Green20', 'tableau.Green20'),
                ('tableau.Red20', 'tableau.Red20'),
                ('tableau.Purple20', 'tableau.Purple20'),
                ('tableau.Brown20', 'tableau.Brown20'),
                ('tableau.Gray20', 'tableau.Gray20'),
                ('tableau.GrayWarm20', 'tableau.GrayWarm20'),
                ('tableau.BlueTeal20', 'tableau.BlueTeal20'),
                ('tableau.OrangeGold20', 'tableau.OrangeGold20'),
                ('tableau.GreenGold20', 'tableau.GreenGold20'),
                ('tableau.RedGold21', 'tableau.RedGold21'),
                ('tableau.Classic10', 'tableau.Classic10'),
                ('tableau.ClassicMedium10', 'tableau.ClassicMedium10'),
                ('tableau.ClassicLight10', 'tableau.ClassicLight10'),
                ('tableau.Classic20', 'tableau.Classic20'),
                ('tableau.ClassicGray5', 'tableau.ClassicGray5'),
                ('tableau.ClassicColorBlind10', 'tableau.ClassicColorBlind10'),
                ('tableau.ClassicTrafficLight9', 'tableau.ClassicTrafficLight9'),
                ('tableau.ClassicPurpleGray6', 'tableau.ClassicPurpleGray6'),
                ('tableau.ClassicPurpleGray12', 'tableau.ClassicPurpleGray12'),
                ('tableau.ClassicGreenOrange6', 'tableau.ClassicGreenOrange6'),
                ('tableau.ClassicGreenOrange12', 'tableau.ClassicGreenOrange12'),
                ('tableau.ClassicBlueRed6', 'tableau.ClassicBlueRed6'),
                ('tableau.ClassicBlueRed12', 'tableau.ClassicBlueRed12'),
                ('tableau.ClassicCyclic13', 'tableau.ClassicCyclic13'),
                ('tableau.ClassicGreen7', 'tableau.ClassicGreen7'),
                ('tableau.ClassicGray13', 'tableau.ClassicGray13'),
                ('tableau.ClassicBlue7', 'tableau.ClassicBlue7'),
                ('tableau.ClassicRed9', 'tableau.ClassicRed9'),
                ('tableau.ClassicOrange7', 'tableau.ClassicOrange7'),
                ('tableau.ClassicAreaRed11', 'tableau.ClassicAreaRed11'),
                ('tableau.ClassicAreaGreen11', 'tableau.ClassicAreaGreen11'),
                ('tableau.ClassicAreaBrown11', 'tableau.ClassicAreaBrown11'),
                ('tableau.ClassicRedGreen11', 'tableau.ClassicRedGreen11'),
                ('tableau.ClassicRedBlue11', 'tableau.ClassicRedBlue11'),
                ('tableau.ClassicRedBlack11', 'tableau.ClassicRedBlack11'),
                ('tableau.ClassicAreaRedGreen21', 'tableau.ClassicAreaRedGreen21'),
                ('tableau.ClassicOrangeBlue13', 'tableau.ClassicOrangeBlue13'),
                ('tableau.ClassicGreenBlue11', 'tableau.ClassicGreenBlue11'),
                ('tableau.ClassicRedWhiteGreen11', 'tableau.ClassicRedWhiteGreen11'),
                ('tableau.ClassicRedWhiteBlack11', 'tableau.ClassicRedWhiteBlack11'),
                ('tableau.ClassicOrangeWhiteBlue11', 'tableau.ClassicOrangeWhiteBlue11'),
                ('tableau.ClassicRedWhiteBlackLight10', 'tableau.ClassicRedWhiteBlackLight10'),
                ('tableau.ClassicOrangeWhiteBlueLight11', 'tableau.ClassicOrangeWhiteBlueLight11'),
                ('tableau.ClassicRedWhiteGreenLight11', 'tableau.ClassicRedWhiteGreenLight11'),
                ('tableau.ClassicRedGreenLight11', 'tableau.ClassicRedGreenLight11')]
COLOR_HEXCODE = [('YlGn3', ['#f7fcb9', '#addd8e', '#31a354']), ('YlGn4', ['#ffffcc', '#c2e699', '#78c679', '#238443']),
                 ('YlGn5', ['#ffffcc', '#c2e699', '#78c679', '#31a354', '#006837']),
                 ('YlGn6', ['#ffffcc', '#d9f0a3', '#addd8e', '#78c679', '#31a354', '#006837']),
                 ('YlGn7', ['#ffffcc', '#d9f0a3', '#addd8e', '#78c679', '#41ab5d', '#238443', '#005a32']),
                 ('YlGn8', ['#ffffe5', '#f7fcb9', '#d9f0a3', '#addd8e', '#78c679', '#41ab5d', '#238443', '#005a32']), (
                 'YlGn9',
                 ['#ffffe5', '#f7fcb9', '#d9f0a3', '#addd8e', '#78c679', '#41ab5d', '#238443', '#006837', '#004529']),
                 ('YlGnBu3', ['#edf8b1', '#7fcdbb', '#2c7fb8']),
                 ('YlGnBu4', ['#ffffcc', '#a1dab4', '#41b6c4', '#225ea8']),
                 ('YlGnBu5', ['#ffffcc', '#a1dab4', '#41b6c4', '#2c7fb8', '#253494']),
                 ('YlGnBu6', ['#ffffcc', '#c7e9b4', '#7fcdbb', '#41b6c4', '#2c7fb8', '#253494']),
                 ('YlGnBu7', ['#ffffcc', '#c7e9b4', '#7fcdbb', '#41b6c4', '#1d91c0', '#225ea8', '#0c2c84']),
                 ('YlGnBu8', ['#ffffd9', '#edf8b1', '#c7e9b4', '#7fcdbb', '#41b6c4', '#1d91c0', '#225ea8', '#0c2c84']),
                 ('YlGnBu9',
                  ['#ffffd9', '#edf8b1', '#c7e9b4', '#7fcdbb', '#41b6c4', '#1d91c0', '#225ea8', '#253494', '#081d58']),
                 ('GnBu3', ['#e0f3db', '#a8ddb5', '#43a2ca']), ('GnBu4', ['#f0f9e8', '#bae4bc', '#7bccc4', '#2b8cbe']),
                 ('GnBu5', ['#f0f9e8', '#bae4bc', '#7bccc4', '#43a2ca', '#0868ac']),
                 ('GnBu6', ['#f0f9e8', '#ccebc5', '#a8ddb5', '#7bccc4', '#43a2ca', '#0868ac']),
                 ('GnBu7', ['#f0f9e8', '#ccebc5', '#a8ddb5', '#7bccc4', '#4eb3d3', '#2b8cbe', '#08589e']),
                 ('GnBu8', ['#f7fcf0', '#e0f3db', '#ccebc5', '#a8ddb5', '#7bccc4', '#4eb3d3', '#2b8cbe', '#08589e']), (
                 'GnBu9',
                 ['#f7fcf0', '#e0f3db', '#ccebc5', '#a8ddb5', '#7bccc4', '#4eb3d3', '#2b8cbe', '#0868ac', '#084081']),
                 ('BuGn3', ['#e5f5f9', '#99d8c9', '#2ca25f']), ('BuGn4', ['#edf8fb', '#b2e2e2', '#66c2a4', '#238b45']),
                 ('BuGn5', ['#edf8fb', '#b2e2e2', '#66c2a4', '#2ca25f', '#006d2c']),
                 ('BuGn6', ['#edf8fb', '#ccece6', '#99d8c9', '#66c2a4', '#2ca25f', '#006d2c']),
                 ('BuGn7', ['#edf8fb', '#ccece6', '#99d8c9', '#66c2a4', '#41ae76', '#238b45', '#005824']),
                 ('BuGn8', ['#f7fcfd', '#e5f5f9', '#ccece6', '#99d8c9', '#66c2a4', '#41ae76', '#238b45', '#005824']), (
                 'BuGn9',
                 ['#f7fcfd', '#e5f5f9', '#ccece6', '#99d8c9', '#66c2a4', '#41ae76', '#238b45', '#006d2c', '#00441b']),
                 ('PuBuGn3', ['#ece2f0', '#a6bddb', '#1c9099']),
                 ('PuBuGn4', ['#f6eff7', '#bdc9e1', '#67a9cf', '#02818a']),
                 ('PuBuGn5', ['#f6eff7', '#bdc9e1', '#67a9cf', '#1c9099', '#016c59']),
                 ('PuBuGn6', ['#f6eff7', '#d0d1e6', '#a6bddb', '#67a9cf', '#1c9099', '#016c59']),
                 ('PuBuGn7', ['#f6eff7', '#d0d1e6', '#a6bddb', '#67a9cf', '#3690c0', '#02818a', '#016450']),
                 ('PuBuGn8', ['#fff7fb', '#ece2f0', '#d0d1e6', '#a6bddb', '#67a9cf', '#3690c0', '#02818a', '#016450']),
                 ('PuBuGn9',
                  ['#fff7fb', '#ece2f0', '#d0d1e6', '#a6bddb', '#67a9cf', '#3690c0', '#02818a', '#016c59', '#014636']),
                 ('PuBu3', ['#ece7f2', '#a6bddb', '#2b8cbe']), ('PuBu4', ['#f1eef6', '#bdc9e1', '#74a9cf', '#0570b0']),
                 ('PuBu5', ['#f1eef6', '#bdc9e1', '#74a9cf', '#2b8cbe', '#045a8d']),
                 ('PuBu6', ['#f1eef6', '#d0d1e6', '#a6bddb', '#74a9cf', '#2b8cbe', '#045a8d']),
                 ('PuBu7', ['#f1eef6', '#d0d1e6', '#a6bddb', '#74a9cf', '#3690c0', '#0570b0', '#034e7b']),
                 ('PuBu8', ['#fff7fb', '#ece7f2', '#d0d1e6', '#a6bddb', '#74a9cf', '#3690c0', '#0570b0', '#034e7b']), (
                 'PuBu9',
                 ['#fff7fb', '#ece7f2', '#d0d1e6', '#a6bddb', '#74a9cf', '#3690c0', '#0570b0', '#045a8d', '#023858']),
                 ('BuPu3', ['#e0ecf4', '#9ebcda', '#8856a7']), ('BuPu4', ['#edf8fb', '#b3cde3', '#8c96c6', '#88419d']),
                 ('BuPu5', ['#edf8fb', '#b3cde3', '#8c96c6', '#8856a7', '#810f7c']),
                 ('BuPu6', ['#edf8fb', '#bfd3e6', '#9ebcda', '#8c96c6', '#8856a7', '#810f7c']),
                 ('BuPu7', ['#edf8fb', '#bfd3e6', '#9ebcda', '#8c96c6', '#8c6bb1', '#88419d', '#6e016b']),
                 ('BuPu8', ['#f7fcfd', '#e0ecf4', '#bfd3e6', '#9ebcda', '#8c96c6', '#8c6bb1', '#88419d', '#6e016b']), (
                 'BuPu9',
                 ['#f7fcfd', '#e0ecf4', '#bfd3e6', '#9ebcda', '#8c96c6', '#8c6bb1', '#88419d', '#810f7c', '#4d004b']),
                 ('RdPu3', ['#fde0dd', '#fa9fb5', '#c51b8a']), ('RdPu4', ['#feebe2', '#fbb4b9', '#f768a1', '#ae017e']),
                 ('RdPu5', ['#feebe2', '#fbb4b9', '#f768a1', '#c51b8a', '#7a0177']),
                 ('RdPu6', ['#feebe2', '#fcc5c0', '#fa9fb5', '#f768a1', '#c51b8a', '#7a0177']),
                 ('RdPu7', ['#feebe2', '#fcc5c0', '#fa9fb5', '#f768a1', '#dd3497', '#ae017e', '#7a0177']),
                 ('RdPu8', ['#fff7f3', '#fde0dd', '#fcc5c0', '#fa9fb5', '#f768a1', '#dd3497', '#ae017e', '#7a0177']), (
                 'RdPu9',
                 ['#fff7f3', '#fde0dd', '#fcc5c0', '#fa9fb5', '#f768a1', '#dd3497', '#ae017e', '#7a0177', '#49006a']),
                 ('PuRd3', ['#e7e1ef', '#c994c7', '#dd1c77']), ('PuRd4', ['#f1eef6', '#d7b5d8', '#df65b0', '#ce1256']),
                 ('PuRd5', ['#f1eef6', '#d7b5d8', '#df65b0', '#dd1c77', '#980043']),
                 ('PuRd6', ['#f1eef6', '#d4b9da', '#c994c7', '#df65b0', '#dd1c77', '#980043']),
                 ('PuRd7', ['#f1eef6', '#d4b9da', '#c994c7', '#df65b0', '#e7298a', '#ce1256', '#91003f']),
                 ('PuRd8', ['#f7f4f9', '#e7e1ef', '#d4b9da', '#c994c7', '#df65b0', '#e7298a', '#ce1256', '#91003f']), (
                 'PuRd9',
                 ['#f7f4f9', '#e7e1ef', '#d4b9da', '#c994c7', '#df65b0', '#e7298a', '#ce1256', '#980043', '#67001f']),
                 ('OrRd3', ['#fee8c8', '#fdbb84', '#e34a33']), ('OrRd4', ['#fef0d9', '#fdcc8a', '#fc8d59', '#d7301f']),
                 ('OrRd5', ['#fef0d9', '#fdcc8a', '#fc8d59', '#e34a33', '#b30000']),
                 ('OrRd6', ['#fef0d9', '#fdd49e', '#fdbb84', '#fc8d59', '#e34a33', '#b30000']),
                 ('OrRd7', ['#fef0d9', '#fdd49e', '#fdbb84', '#fc8d59', '#ef6548', '#d7301f', '#990000']),
                 ('OrRd8', ['#fff7ec', '#fee8c8', '#fdd49e', '#fdbb84', '#fc8d59', '#ef6548', '#d7301f', '#990000']), (
                 'OrRd9',
                 ['#fff7ec', '#fee8c8', '#fdd49e', '#fdbb84', '#fc8d59', '#ef6548', '#d7301f', '#b30000', '#7f0000']),
                 ('YlOrRd3', ['#ffeda0', '#feb24c', '#f03b20']),
                 ('YlOrRd4', ['#ffffb2', '#fecc5c', '#fd8d3c', '#e31a1c']),
                 ('YlOrRd5', ['#ffffb2', '#fecc5c', '#fd8d3c', '#f03b20', '#bd0026']),
                 ('YlOrRd6', ['#ffffb2', '#fed976', '#feb24c', '#fd8d3c', '#f03b20', '#bd0026']),
                 ('YlOrRd7', ['#ffffb2', '#fed976', '#feb24c', '#fd8d3c', '#fc4e2a', '#e31a1c', '#b10026']),
                 ('YlOrRd8', ['#ffffcc', '#ffeda0', '#fed976', '#feb24c', '#fd8d3c', '#fc4e2a', '#e31a1c', '#b10026']),
                 ('YlOrRd9',
                  ['#ffffcc', '#ffeda0', '#fed976', '#feb24c', '#fd8d3c', '#fc4e2a', '#e31a1c', '#bd0026', '#800026']),
                 ('YlOrBr3', ['#fff7bc', '#fec44f', '#d95f0e']),
                 ('YlOrBr4', ['#ffffd4', '#fed98e', '#fe9929', '#cc4c02']),
                 ('YlOrBr5', ['#ffffd4', '#fed98e', '#fe9929', '#d95f0e', '#993404']),
                 ('YlOrBr6', ['#ffffd4', '#fee391', '#fec44f', '#fe9929', '#d95f0e', '#993404']),
                 ('YlOrBr7', ['#ffffd4', '#fee391', '#fec44f', '#fe9929', '#ec7014', '#cc4c02', '#8c2d04']),
                 ('YlOrBr8', ['#ffffe5', '#fff7bc', '#fee391', '#fec44f', '#fe9929', '#ec7014', '#cc4c02', '#8c2d04']),
                 ('YlOrBr9',
                  ['#ffffe5', '#fff7bc', '#fee391', '#fec44f', '#fe9929', '#ec7014', '#cc4c02', '#993404', '#662506']),
                 ('Purples3', ['#efedf5', '#bcbddc', '#756bb1']),
                 ('Purples4', ['#f2f0f7', '#cbc9e2', '#9e9ac8', '#6a51a3']),
                 ('Purples5', ['#f2f0f7', '#cbc9e2', '#9e9ac8', '#756bb1', '#54278f']),
                 ('Purples6', ['#f2f0f7', '#dadaeb', '#bcbddc', '#9e9ac8', '#756bb1', '#54278f']),
                 ('Purples7', ['#f2f0f7', '#dadaeb', '#bcbddc', '#9e9ac8', '#807dba', '#6a51a3', '#4a1486']),
                 ('Purples8', ['#fcfbfd', '#efedf5', '#dadaeb', '#bcbddc', '#9e9ac8', '#807dba', '#6a51a3', '#4a1486']),
                 ('Purples9',
                  ['#fcfbfd', '#efedf5', '#dadaeb', '#bcbddc', '#9e9ac8', '#807dba', '#6a51a3', '#54278f', '#3f007d']),
                 ('Blues3', ['#deebf7', '#9ecae1', '#3182bd']),
                 ('Blues4', ['#eff3ff', '#bdd7e7', '#6baed6', '#2171b5']),
                 ('Blues5', ['#eff3ff', '#bdd7e7', '#6baed6', '#3182bd', '#08519c']),
                 ('Blues6', ['#eff3ff', '#c6dbef', '#9ecae1', '#6baed6', '#3182bd', '#08519c']),
                 ('Blues7', ['#eff3ff', '#c6dbef', '#9ecae1', '#6baed6', '#4292c6', '#2171b5', '#084594']),
                 ('Blues8', ['#f7fbff', '#deebf7', '#c6dbef', '#9ecae1', '#6baed6', '#4292c6', '#2171b5', '#084594']), (
                 'Blues9',
                 ['#f7fbff', '#deebf7', '#c6dbef', '#9ecae1', '#6baed6', '#4292c6', '#2171b5', '#08519c', '#08306b']),
                 ('Greens3', ['#e5f5e0', '#a1d99b', '#31a354']),
                 ('Greens4', ['#edf8e9', '#bae4b3', '#74c476', '#238b45']),
                 ('Greens5', ['#edf8e9', '#bae4b3', '#74c476', '#31a354', '#006d2c']),
                 ('Greens6', ['#edf8e9', '#c7e9c0', '#a1d99b', '#74c476', '#31a354', '#006d2c']),
                 ('Greens7', ['#edf8e9', '#c7e9c0', '#a1d99b', '#74c476', '#41ab5d', '#238b45', '#005a32']),
                 ('Greens8', ['#f7fcf5', '#e5f5e0', '#c7e9c0', '#a1d99b', '#74c476', '#41ab5d', '#238b45', '#005a32']),
                 ('Greens9',
                  ['#f7fcf5', '#e5f5e0', '#c7e9c0', '#a1d99b', '#74c476', '#41ab5d', '#238b45', '#006d2c', '#00441b']),
                 ('Oranges3', ['#fee6ce', '#fdae6b', '#e6550d']),
                 ('Oranges4', ['#feedde', '#fdbe85', '#fd8d3c', '#d94701']),
                 ('Oranges5', ['#feedde', '#fdbe85', '#fd8d3c', '#e6550d', '#a63603']),
                 ('Oranges6', ['#feedde', '#fdd0a2', '#fdae6b', '#fd8d3c', '#e6550d', '#a63603']),
                 ('Oranges7', ['#feedde', '#fdd0a2', '#fdae6b', '#fd8d3c', '#f16913', '#d94801', '#8c2d04']),
                 ('Oranges8', ['#fff5eb', '#fee6ce', '#fdd0a2', '#fdae6b', '#fd8d3c', '#f16913', '#d94801', '#8c2d04']),
                 ('Oranges9',
                  ['#fff5eb', '#fee6ce', '#fdd0a2', '#fdae6b', '#fd8d3c', '#f16913', '#d94801', '#a63603', '#7f2704']),
                 ('Reds3', ['#fee0d2', '#fc9272', '#de2d26']), ('Reds4', ['#fee5d9', '#fcae91', '#fb6a4a', '#cb181d']),
                 ('Reds5', ['#fee5d9', '#fcae91', '#fb6a4a', '#de2d26', '#a50f15']),
                 ('Reds6', ['#fee5d9', '#fcbba1', '#fc9272', '#fb6a4a', '#de2d26', '#a50f15']),
                 ('Reds7', ['#fee5d9', '#fcbba1', '#fc9272', '#fb6a4a', '#ef3b2c', '#cb181d', '#99000d']),
                 ('Reds8', ['#fff5f0', '#fee0d2', '#fcbba1', '#fc9272', '#fb6a4a', '#ef3b2c', '#cb181d', '#99000d']), (
                 'Reds9',
                 ['#fff5f0', '#fee0d2', '#fcbba1', '#fc9272', '#fb6a4a', '#ef3b2c', '#cb181d', '#a50f15', '#67000d']),
                 ('Greys3', ['#f0f0f0', '#bdbdbd', '#636363']),
                 ('Greys4', ['#f7f7f7', '#cccccc', '#969696', '#525252']),
                 ('Greys5', ['#f7f7f7', '#cccccc', '#969696', '#636363', '#252525']),
                 ('Greys6', ['#f7f7f7', '#d9d9d9', '#bdbdbd', '#969696', '#636363', '#252525']),
                 ('Greys7', ['#f7f7f7', '#d9d9d9', '#bdbdbd', '#969696', '#737373', '#525252', '#252525']),
                 ('Greys8', ['#ffffff', '#f0f0f0', '#d9d9d9', '#bdbdbd', '#969696', '#737373', '#525252', '#252525']), (
                 'Greys9',
                 ['#ffffff', '#f0f0f0', '#d9d9d9', '#bdbdbd', '#969696', '#737373', '#525252', '#252525', '#000000']),
                 ('PuOr3', ['#f1a340', '#f7f7f7', '#998ec3']), ('PuOr4', ['#e66101', '#fdb863', '#b2abd2', '#5e3c99']),
                 ('PuOr5', ['#e66101', '#fdb863', '#f7f7f7', '#b2abd2', '#5e3c99']),
                 ('PuOr6', ['#b35806', '#f1a340', '#fee0b6', '#d8daeb', '#998ec3', '#542788']),
                 ('PuOr7', ['#b35806', '#f1a340', '#fee0b6', '#f7f7f7', '#d8daeb', '#998ec3', '#542788']),
                 ('PuOr8', ['#b35806', '#e08214', '#fdb863', '#fee0b6', '#d8daeb', '#b2abd2', '#8073ac', '#542788']), (
                 'PuOr9',
                 ['#b35806', '#e08214', '#fdb863', '#fee0b6', '#f7f7f7', '#d8daeb', '#b2abd2', '#8073ac', '#542788']), (
                 'PuOr10',
                 ['#7f3b08', '#b35806', '#e08214', '#fdb863', '#fee0b6', '#d8daeb', '#b2abd2', '#8073ac', '#542788',
                  '#2d004b']), ('PuOr11',
                                ['#7f3b08', '#b35806', '#e08214', '#fdb863', '#fee0b6', '#f7f7f7', '#d8daeb', '#b2abd2',
                                 '#8073ac', '#542788', '#2d004b']), ('BrBG3', ['#d8b365', '#f5f5f5', '#5ab4ac']),
                 ('BrBG4', ['#a6611a', '#dfc27d', '#80cdc1', '#018571']),
                 ('BrBG5', ['#a6611a', '#dfc27d', '#f5f5f5', '#80cdc1', '#018571']),
                 ('BrBG6', ['#8c510a', '#d8b365', '#f6e8c3', '#c7eae5', '#5ab4ac', '#01665e']),
                 ('BrBG7', ['#8c510a', '#d8b365', '#f6e8c3', '#f5f5f5', '#c7eae5', '#5ab4ac', '#01665e']),
                 ('BrBG8', ['#8c510a', '#bf812d', '#dfc27d', '#f6e8c3', '#c7eae5', '#80cdc1', '#35978f', '#01665e']), (
                 'BrBG9',
                 ['#8c510a', '#bf812d', '#dfc27d', '#f6e8c3', '#f5f5f5', '#c7eae5', '#80cdc1', '#35978f', '#01665e']), (
                 'BrBG10',
                 ['#543005', '#8c510a', '#bf812d', '#dfc27d', '#f6e8c3', '#c7eae5', '#80cdc1', '#35978f', '#01665e',
                  '#003c30']), ('BrBG11',
                                ['#543005', '#8c510a', '#bf812d', '#dfc27d', '#f6e8c3', '#f5f5f5', '#c7eae5', '#80cdc1',
                                 '#35978f', '#01665e', '#003c30']), ('PRGn3', ['#af8dc3', '#f7f7f7', '#7fbf7b']),
                 ('PRGn4', ['#7b3294', '#c2a5cf', '#a6dba0', '#008837']),
                 ('PRGn5', ['#7b3294', '#c2a5cf', '#f7f7f7', '#a6dba0', '#008837']),
                 ('PRGn6', ['#762a83', '#af8dc3', '#e7d4e8', '#d9f0d3', '#7fbf7b', '#1b7837']),
                 ('PRGn7', ['#762a83', '#af8dc3', '#e7d4e8', '#f7f7f7', '#d9f0d3', '#7fbf7b', '#1b7837']),
                 ('PRGn8', ['#762a83', '#9970ab', '#c2a5cf', '#e7d4e8', '#d9f0d3', '#a6dba0', '#5aae61', '#1b7837']), (
                 'PRGn9',
                 ['#762a83', '#9970ab', '#c2a5cf', '#e7d4e8', '#f7f7f7', '#d9f0d3', '#a6dba0', '#5aae61', '#1b7837']), (
                 'PRGn10',
                 ['#40004b', '#762a83', '#9970ab', '#c2a5cf', '#e7d4e8', '#d9f0d3', '#a6dba0', '#5aae61', '#1b7837',
                  '#00441b']), ('PRGn11',
                                ['#40004b', '#762a83', '#9970ab', '#c2a5cf', '#e7d4e8', '#f7f7f7', '#d9f0d3', '#a6dba0',
                                 '#5aae61', '#1b7837', '#00441b']), ('PiYG3', ['#e9a3c9', '#f7f7f7', '#a1d76a']),
                 ('PiYG4', ['#d01c8b', '#f1b6da', '#b8e186', '#4dac26']),
                 ('PiYG5', ['#d01c8b', '#f1b6da', '#f7f7f7', '#b8e186', '#4dac26']),
                 ('PiYG6', ['#c51b7d', '#e9a3c9', '#fde0ef', '#e6f5d0', '#a1d76a', '#4d9221']),
                 ('PiYG7', ['#c51b7d', '#e9a3c9', '#fde0ef', '#f7f7f7', '#e6f5d0', '#a1d76a', '#4d9221']),
                 ('PiYG8', ['#c51b7d', '#de77ae', '#f1b6da', '#fde0ef', '#e6f5d0', '#b8e186', '#7fbc41', '#4d9221']), (
                 'PiYG9',
                 ['#c51b7d', '#de77ae', '#f1b6da', '#fde0ef', '#f7f7f7', '#e6f5d0', '#b8e186', '#7fbc41', '#4d9221']), (
                 'PiYG10',
                 ['#8e0152', '#c51b7d', '#de77ae', '#f1b6da', '#fde0ef', '#e6f5d0', '#b8e186', '#7fbc41', '#4d9221',
                  '#276419']), ('PiYG11',
                                ['#8e0152', '#c51b7d', '#de77ae', '#f1b6da', '#fde0ef', '#f7f7f7', '#e6f5d0', '#b8e186',
                                 '#7fbc41', '#4d9221', '#276419']), ('RdBu3', ['#ef8a62', '#f7f7f7', '#67a9cf']),
                 ('RdBu4', ['#ca0020', '#f4a582', '#92c5de', '#0571b0']),
                 ('RdBu5', ['#ca0020', '#f4a582', '#f7f7f7', '#92c5de', '#0571b0']),
                 ('RdBu6', ['#b2182b', '#ef8a62', '#fddbc7', '#d1e5f0', '#67a9cf', '#2166ac']),
                 ('RdBu7', ['#b2182b', '#ef8a62', '#fddbc7', '#f7f7f7', '#d1e5f0', '#67a9cf', '#2166ac']),
                 ('RdBu8', ['#b2182b', '#d6604d', '#f4a582', '#fddbc7', '#d1e5f0', '#92c5de', '#4393c3', '#2166ac']), (
                 'RdBu9',
                 ['#b2182b', '#d6604d', '#f4a582', '#fddbc7', '#f7f7f7', '#d1e5f0', '#92c5de', '#4393c3', '#2166ac']), (
                 'RdBu10',
                 ['#67001f', '#b2182b', '#d6604d', '#f4a582', '#fddbc7', '#d1e5f0', '#92c5de', '#4393c3', '#2166ac',
                  '#053061']), ('RdBu11',
                                ['#67001f', '#b2182b', '#d6604d', '#f4a582', '#fddbc7', '#f7f7f7', '#d1e5f0', '#92c5de',
                                 '#4393c3', '#2166ac', '#053061']), ('RdGy3', ['#ef8a62', '#ffffff', '#999999']),
                 ('RdGy4', ['#ca0020', '#f4a582', '#bababa', '#404040']),
                 ('RdGy5', ['#ca0020', '#f4a582', '#ffffff', '#bababa', '#404040']),
                 ('RdGy6', ['#b2182b', '#ef8a62', '#fddbc7', '#e0e0e0', '#999999', '#4d4d4d']),
                 ('RdGy7', ['#b2182b', '#ef8a62', '#fddbc7', '#ffffff', '#e0e0e0', '#999999', '#4d4d4d']),
                 ('RdGy8', ['#b2182b', '#d6604d', '#f4a582', '#fddbc7', '#e0e0e0', '#bababa', '#878787', '#4d4d4d']),
                 ('RdGy9',
                  ['#b2182b', '#d6604d', '#f4a582', '#fddbc7', '#ffffff', '#e0e0e0', '#bababa', '#878787', '#4d4d4d']),
                 ('RdGy10',
                  ['#67001f', '#b2182b', '#d6604d', '#f4a582', '#fddbc7', '#e0e0e0', '#bababa', '#878787', '#4d4d4d',
                   '#1a1a1a']),
                 ('RdGy11',
                  ['#67001f', '#b2182b', '#d6604d', '#f4a582', '#fddbc7', '#ffffff', '#e0e0e0', '#bababa', '#878787',
                   '#4d4d4d',
                   '#1a1a1a']),

                 ('RdYlBu3', ['#fc8d59', '#ffffbf', '#91bfdb']),
                 ('RdYlBu4', ['#d7191c', '#fdae61', '#abd9e9', '#2c7bb6']),
                 ('RdYlBu5', ['#d7191c', '#fdae61', '#ffffbf', '#abd9e9', '#2c7bb6']),
                 ('RdYlBu6', ['#d73027', '#fc8d59', '#fee090', '#e0f3f8', '#91bfdb', '#4575b4']),
                 ('RdYlBu7', ['#d73027', '#fc8d59', '#fee090', '#ffffbf', '#e0f3f8', '#91bfdb', '#4575b4']),
                 ('RdYlBu8', ['#d73027', '#f46d43', '#fdae61', '#fee090', '#e0f3f8', '#abd9e9', '#74add1', '#4575b4']),
                 ('RdYlBu9',
                  ['#d73027', '#f46d43', '#fdae61', '#fee090', '#ffffbf', '#e0f3f8', '#abd9e9', '#74add1', '#4575b4']),
                 ('RdYlBu10',
                  ['#a50026', '#d73027', '#f46d43', '#fdae61', '#fee090', '#e0f3f8', '#abd9e9', '#74add1', '#4575b4',
                   '#313695']),
                 ('RdYlBu11',
                  ['#a50026', '#d73027', '#f46d43', '#fdae61', '#fee090', '#ffffbf', '#e0f3f8', '#abd9e9', '#74add1',
                   '#4575b4',
                   '#313695']),

                 ('Spectral3', ['#fc8d59', '#ffffbf', '#99d594']),
                 ('Spectral4', ['#d7191c', '#fdae61', '#abdda4', '#2b83ba']),
                 ('Spectral5', ['#d7191c', '#fdae61', '#ffffbf', '#abdda4', '#2b83ba']),
                 ('Spectral6', ['#d53e4f', '#fc8d59', '#fee08b', '#e6f598', '#99d594', '#3288bd']),
                 ('Spectral7', ['#d53e4f', '#fc8d59', '#fee08b', '#ffffbf', '#e6f598', '#99d594', '#3288bd']),
                 (
                     'Spectral8',
                     ['#d53e4f', '#f46d43', '#fdae61', '#fee08b', '#e6f598', '#abdda4', '#66c2a5', '#3288bd']),
                 ('Spectral9',
                  ['#d53e4f', '#f46d43', '#fdae61', '#fee08b', '#ffffbf', '#e6f598', '#abdda4', '#66c2a5', '#3288bd']),
                 ('Spectral10',
                  ['#9e0142', '#d53e4f', '#f46d43', '#fdae61', '#fee08b', '#e6f598', '#abdda4', '#66c2a5', '#3288bd',
                   '#5e4fa2']),
                 ('Spectral11',
                  ['#9e0142', '#d53e4f', '#f46d43', '#fdae61', '#fee08b', '#ffffbf', '#e6f598', '#abdda4', '#66c2a5',
                   '#3288bd',
                   '#5e4fa2']),

                 ('RdYlGn3', ['#fc8d59', '#ffffbf', '#91cf60']),
                 ('RdYlGn4', ['#d7191c', '#fdae61', '#a6d96a', '#1a9641']),
                 ('RdYlGn5', ['#d7191c', '#fdae61', '#ffffbf', '#a6d96a', '#1a9641']),
                 ('RdYlGn6', ['#d73027', '#fc8d59', '#fee08b', '#d9ef8b', '#91cf60', '#1a9850']),
                 ('RdYlGn7', ['#d73027', '#fc8d59', '#fee08b', '#ffffbf', '#d9ef8b', '#91cf60', '#1a9850']),
                 ('RdYlGn8', ['#d73027', '#f46d43', '#fdae61', '#fee08b', '#d9ef8b', '#a6d96a', '#66bd63', '#1a9850']),
                 ('RdYlGn9',
                  ['#d73027', '#f46d43', '#fdae61', '#fee08b', '#ffffbf', '#d9ef8b', '#a6d96a', '#66bd63', '#1a9850']),
                 ('RdYlGn10',
                  ['#a50026', '#d73027', '#f46d43', '#fdae61', '#fee08b', '#d9ef8b', '#a6d96a', '#66bd63', '#1a9850',
                   '#006837']),
                 ('RdYlGn11',
                  ['#a50026', '#d73027', '#f46d43', '#fdae61', '#fee08b', '#ffffbf', '#d9ef8b', '#a6d96a', '#66bd63',
                   '#1a9850',
                   '#006837']),

                 ('Accent3', ['#7fc97f', '#beaed4', '#fdc086']),
                 ('Accent4', ['#7fc97f', '#beaed4', '#fdc086', '#ffff99']),
                 ('Accent5', ['#7fc97f', '#beaed4', '#fdc086', '#ffff99', '#386cb0']),
                 ('Accent6', ['#7fc97f', '#beaed4', '#fdc086', '#ffff99', '#386cb0', '#f0027f']),
                 ('Accent7', ['#7fc97f', '#beaed4', '#fdc086', '#ffff99', '#386cb0', '#f0027f', '#bf5b17']),
                 ('Accent8', ['#7fc97f', '#beaed4', '#fdc086', '#ffff99', '#386cb0', '#f0027f', '#bf5b17', '#666666']),

                 ('DarkTwo3', ['#1b9e77', '#d95f02', '#7570b3']),
                 ('DarkTwo4', ['#1b9e77', '#d95f02', '#7570b3', '#e7298a']),
                 ('DarkTwo5', ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e']),
                 ('DarkTwo6', ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e', '#e6ab02']),
                 ('DarkTwo7', ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e', '#e6ab02', '#a6761d']),
                 ('DarkTwo8', ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e', '#e6ab02', '#a6761d', '#666666']),

                 ('Paired3', ['#a6cee3', '#1f78b4', '#b2df8a']),
                 ('Paired4', ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c']),
                 ('Paired5', ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99']),
                 ('Paired6', ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c']),
                 ('Paired7', ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f']),
                 ('Paired8', ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00']),
                 ('Paired9',
                  ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6']),
                 ('Paired10',
                  ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6',
                   '#6a3d9a']),
                 ('Paired11',
                  ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6',
                   '#6a3d9a',
                   '#ffff99']),
                 ('Paired12',
                  ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6',
                   '#6a3d9a',
                   '#ffff99', '#b15928']),

                 ('PastelOne3', ['#fbb4ae', '#b3cde3', '#ccebc5']),
                 ('PastelOne4', ['#fbb4ae', '#b3cde3', '#ccebc5', '#decbe4']),
                 ('PastelOne5', ['#fbb4ae', '#b3cde3', '#ccebc5', '#decbe4', '#fed9a6']),
                 ('PastelOne6', ['#fbb4ae', '#b3cde3', '#ccebc5', '#decbe4', '#fed9a6', '#ffffcc']),
                 ('PastelOne7', ['#fbb4ae', '#b3cde3', '#ccebc5', '#decbe4', '#fed9a6', '#ffffcc', '#e5d8bd']),
                 ('PastelOne8',
                  ['#fbb4ae', '#b3cde3', '#ccebc5', '#decbe4', '#fed9a6', '#ffffcc', '#e5d8bd', '#fddaec']),
                 (
                     'PastelOne9',
                     ['#fbb4ae', '#b3cde3', '#ccebc5', '#decbe4', '#fed9a6', '#ffffcc', '#e5d8bd', '#fddaec',
                      '#f2f2f2']),

                 ('PastelTwo3', ['#b3e2cd', '#fdcdac', '#cbd5e8']),
                 ('PastelTwo4', ['#b3e2cd', '#fdcdac', '#cbd5e8', '#f4cae4']),
                 ('PastelTwo5', ['#b3e2cd', '#fdcdac', '#cbd5e8', '#f4cae4', '#e6f5c9']),
                 ('PastelTwo6', ['#b3e2cd', '#fdcdac', '#cbd5e8', '#f4cae4', '#e6f5c9', '#fff2ae']),
                 ('PastelTwo7', ['#b3e2cd', '#fdcdac', '#cbd5e8', '#f4cae4', '#e6f5c9', '#fff2ae', '#f1e2cc']),
                 ('PastelTwo8',
                  ['#b3e2cd', '#fdcdac', '#cbd5e8', '#f4cae4', '#e6f5c9', '#fff2ae', '#f1e2cc', '#cccccc']),

                 ('SetOne3', ['#e41a1c', '#377eb8', '#4daf4a']),
                 ('SetOne4', ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3']),
                 ('SetOne5', ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00']),
                 ('SetOne6', ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33']),
                 ('SetOne7', ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33', '#a65628']),
                 ('SetOne8', ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33', '#a65628', '#f781bf']),
                 ('SetOne9',
                  ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33', '#a65628', '#f781bf', '#999999']),

                 ('SetTwo3', ['#66c2a5', '#fc8d62', '#8da0cb']),
                 ('SetTwo4', ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3']),
                 ('SetTwo5', ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854']),
                 ('SetTwo6', ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854', '#ffd92f']),
                 ('SetTwo7', ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854', '#ffd92f', '#e5c494']),
                 ('SetTwo8', ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854', '#ffd92f', '#e5c494', '#b3b3b3']),

                 ('SetThree3', ['#8dd3c7', '#ffffb3', '#bebada']),
                 ('SetThree4', ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072']),
                 ('SetThree5', ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3']),
                 ('SetThree6', ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3', '#fdb462']),
                 ('SetThree7', ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3', '#fdb462', '#b3de69']),
                 (
                     'SetThree8',
                     ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3', '#fdb462', '#b3de69', '#fccde5']),
                 ('SetThree9',
                  ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3', '#fdb462', '#b3de69', '#fccde5', '#d9d9d9']),
                 ('SetThree10',
                  ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3', '#fdb462', '#b3de69', '#fccde5', '#d9d9d9',
                   '#bc80bd']),
                 ('SetThree11',
                  ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3', '#fdb462', '#b3de69', '#fccde5', '#d9d9d9',
                   '#bc80bd',
                   '#ccebc5']),
                 ('SetThree12',
                  ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3', '#fdb462', '#b3de69', '#fccde5', '#d9d9d9',
                   '#bc80bd',
                   '#ccebc5', '#ffed6f']),
                 ('Adjacency6', ['#a9a57c', '#9cbebd', '#d2cb6c', '#95a39d', '#c89f5d', '#b1a089']),
                 ('Advantage6', ['#663366', '#330f42', '#666699', '#999966', '#f7901e', '#a3a101']),
                 ('Angles6', ['#797b7e', '#f96a1b', '#08a1d9', '#7c984a', '#c2ad8d', '#506e94']),
                 ('Apex6', ['#ceb966', '#9cb084', '#6bb1c9', '#6585cf', '#7e6bc9', '#a379bb']),
                 ('Apothecary6', ['#93a299', '#cf543f', '#b5ae53', '#848058', '#e8b54d', '#786c71']),
                 ('Aspect6', ['#f07f09', '#9f2936', '#1b587c', '#4e8542', '#604878', '#c19859']),
                 ('Atlas6', ['#f81b02', '#fc7715', '#afbf41', '#50c49f', '#3b95c4', '#b560d4']),
                 ('Austin6', ['#94c600', '#71685a', '#ff6700', '#909465', '#956b43', '#fea022']),
                 ('Badge6', ['#f8b323', '#656a59', '#46b2b5', '#8caa7e', '#d36f68', '#826276']),
                 ('Banded6', ['#ffc000', '#a5d028', '#08cc78', '#f24099', '#828288', '#f56617']),
                 ('Basis6', ['#f09415', '#c1b56b', '#4baf73', '#5aa6c0', '#d17df9', '#fa7e5c']),
                 ('Berlin6', ['#a6b727', '#df5327', '#fe9e00', '#418ab3', '#d7d447', '#818183']),
                 ('BlackTie6', ['#6f6f74', '#a7b789', '#beae98', '#92a9b9', '#9c8265', '#8d6974']),
                 ('Blue6', ['#0f6fc6', '#009dd9', '#0bd0d9', '#10cf9b', '#7cca62', '#a5c249']),
                 ('BlueGreen6', ['#3494ba', '#58b6c0', '#75bda7', '#7a8c8e', '#84acb6', '#2683c6']),
                 ('BlueII6', ['#1cade4', '#2683c6', '#27ced7', '#42ba97', '#3e8853', '#62a39f']),
                 ('BlueRed6', ['#4a66ac', '#629dd1', '#297fd5', '#7f8fa9', '#5aa2ae', '#9d90a0']),
                 ('BlueWarm6', ['#4a66ac', '#629dd1', '#297fd5', '#7f8fa9', '#5aa2ae', '#9d90a0']),
                 ('Breeze6', ['#2c7c9f', '#244a58', '#e2751d', '#ffb400', '#7eb606', '#c00000']),
                 ('Capital6', ['#4b5a60', '#9c5238', '#504539', '#c1ad79', '#667559', '#bad6ad']),
                 ('Celestial6', ['#ac3ec1', '#477bd1', '#46b298', '#90ba4c', '#dd9d31', '#e25247']),
                 ('Circuit6', ['#9acd4c', '#faa93a', '#d35940', '#b258d3', '#63a0cc', '#8ac4a7']),
                 ('Civic6', ['#d16349', '#ccb400', '#8cadae', '#8c7b70', '#8fb08c', '#d19049']),
                 ('Clarity6', ['#93a299', '#ad8f67', '#726056', '#4c5a6a', '#808da0', '#79463d']),
                 ('Codex6', ['#990000', '#efab16', '#78ac35', '#35aca2', '#4083cf', '#0d335e']),
                 ('Composite6', ['#98c723', '#59b0b9', '#deae00', '#b77bb4', '#e0773c', '#a98d63']),
                 ('Concourse6', ['#2da2bf', '#da1f28', '#eb641b', '#39639d', '#474b78', '#7d3c4a']),
                 ('Couture6', ['#9e8e5c', '#a09781', '#85776d', '#aeafa9', '#8d878b', '#6b6149']),
                 ('Crop6', ['#8c8d86', '#e6c069', '#897b61', '#8dab8e', '#77a2bb', '#e28394']),
                 ('Damask6', ['#9ec544', '#50bea3', '#4a9ccc', '#9a66ca', '#c54f71', '#de9c3c']),
                 ('Depth6', ['#41aebd', '#97e9d5', '#a2cf49', '#608f3d', '#f4de3a', '#fcb11c']),
                 ('Dividend6', ['#4d1434', '#903163', '#b2324b', '#969fa7', '#66b1ce', '#40619d']),
                 ('Droplet6', ['#2fa3ee', '#4bcaad', '#86c157', '#d99c3f', '#ce6633', '#a35dd1']),
                 ('Elemental6', ['#629dd1', '#297fd5', '#7f8fa9', '#4a66ac', '#5aa2ae', '#9d90a0']),
                 ('Equity6', ['#d34817', '#9b2d1f', '#a28e6a', '#956251', '#918485', '#855d5d']),
                 ('Essential6', ['#7a7a7a', '#f5c201', '#526db0', '#989aac', '#dc5924', '#b4b392']),
                 ('Excel16',
                  ['#9999ff', '#993366', '#ffffcc', '#ccffff', '#660066', '#ff8080', '#0066cc', '#ccccff', '#000080',
                   '#ff00ff',
                   '#ffff00', '#0000ff', '#800080', '#800000', '#008080', '#0000ff']),
                 ('Executive6', ['#6076b4', '#9c5252', '#e68422', '#846648', '#63891f', '#758085']),
                 ('Exhibit6', ['#3399ff', '#69ffff', '#ccff33', '#3333ff', '#9933ff', '#ff33ff']),
                 ('Expo6', ['#fbc01e', '#efe1a2', '#fa8716', '#be0204', '#640f10', '#7e13e3']),
                 ('Facet6', ['#90c226', '#54a021', '#e6b91e', '#e76618', '#c42f1a', '#918655']),
                 ('Feathered6', ['#606372', '#79a8a4', '#b2ad8f', '#ad8082', '#dec18c', '#92a185']),
                 ('Flow6', ['#0f6fc6', '#009dd9', '#0bd0d9', '#10cf9b', '#7cca62', '#a5c249']),
                 ('Focus6', ['#ffb91d', '#f97817', '#6de304', '#ff0000', '#732bea', '#c913ad']),
                 ('Folio6', ['#294171', '#748cbc', '#8e887c', '#834736', '#5a1705', '#a0a16a']),
                 ('Formal6', ['#907f76', '#a46645', '#cd9c47', '#9a92cd', '#7d639b', '#733678']),
                 ('Forte6', ['#c70f0c', '#dd6b0d', '#faa700', '#93e50d', '#17c7ba', '#0a96e4']),
                 ('Foundry6', ['#72a376', '#b0ccb0', '#a8cdd7', '#c0beaf', '#cec597', '#e8b7b7']),
                 ('Frame6', ['#40bad2', '#fab900', '#90bb23', '#ee7008', '#1ab39f', '#d5393d']),
                 ('Gallery6', ['#b71e42', '#de478e', '#bc72f0', '#795faf', '#586ea6', '#6892a0']),
                 ('Genesis6', ['#80b606', '#e29f1d', '#2397e2', '#35aca2', '#5430bb', '#8d34e0']),
                 ('Grayscale6', ['#dddddd', '#b2b2b2', '#969696', '#808080', '#5f5f5f', '#4d4d4d']),
                 ('Green6', ['#549e39', '#8ab833', '#c0cf3a', '#029676', '#4ab5c4', '#0989b1']),
                 ('GreenYellow6', ['#99cb38', '#63a537', '#37a76f', '#44c1a3', '#4eb3cf', '#51c3f9']),
                 ('Grid6', ['#c66951', '#bf974d', '#928b70', '#87706b', '#94734e', '#6f777d']),
                 ('Habitat6', ['#f8c000', '#f88600', '#f83500', '#8b723d', '#818b3d', '#586215']),
                 ('Hardcover6', ['#873624', '#d6862d', '#d0be40', '#877f6c', '#972109', '#aeb795']),
                 ('Headlines6', ['#439eb7', '#e28b55', '#dcb64d', '#4ca198', '#835b82', '#645135']),
                 ('Horizon6', ['#7e97ad', '#cc8e60', '#7a6a60', '#b4936d', '#67787b', '#9d936f']),
                 ('Infusion6', ['#8c73d0', '#c2e8c4', '#c5a6e8', '#b45ec7', '#9fdafb', '#95c5b0']),
                 ('Inkwell6', ['#860908', '#4a0505', '#7a500a', '#c47810', '#827752', '#b5bb83']),
                 ('Inspiration6', ['#749805', '#bacc82', '#6e9ec2', '#2046a5', '#5039c6', '#7411d0']),
                 ('Integral6', ['#1cade4', '#2683c6', '#27ced7', '#42ba97', '#3e8853', '#62a39f']),
                 ('Ion6', ['#b01513', '#ea6312', '#e6b729', '#6aac90', '#5f9c9d', '#9e5e9b']),
                 ('IonBoardroom6', ['#b31166', '#e33d6f', '#e45f3c', '#e9943a', '#9b6bf2', '#d53dd0']),
                 ('Kilter6', ['#76c5ef', '#fea022', '#ff6700', '#70a525', '#a5d848', '#20768c']),
                 ('Madison6', ['#a1d68b', '#5ec795', '#4dadcf', '#cdb756', '#e29c36', '#8ec0c1']),
                 ('MainEvent6', ['#b80e0f', '#a6987d', '#7f9a71', '#64969f', '#9b75b2', '#80737a']),
                 ('Marquee6', ['#418ab3', '#a6b727', '#f69200', '#838383', '#fec306', '#df5327']),
                 ('Median6', ['#94b6d2', '#dd8047', '#a5ab81', '#d8b25c', '#7ba79d', '#968c8c']),
                 ('Mesh6', ['#6f6f6f', '#bfbfa5', '#dcd084', '#e7bf5f', '#e9a039', '#cf7133']),
                 ('Metail6', ['#6283ad', '#324966', '#5b9ea4', '#1d5b57', '#1b4430', '#2f3c35']),
                 ('Metro6', ['#7fd13b', '#ea157a', '#feb80a', '#00addc', '#738ac8', '#1ab39f']),
                 ('Metropolitan6', ['#50b4c8', '#a8b97f', '#9b9256', '#657689', '#7a855d', '#84ac9d']),
                 ('Module6', ['#f0ad00', '#60b5cc', '#e66c7d', '#6bb76d', '#e88651', '#c64847']),
                 ('NewsPrint6', ['#ad0101', '#726056', '#ac956e', '#808da9', '#424e5b', '#730e00']),
                 ('Office6', ['#5b9bd5', '#ed7d31', '#a5a5a5', '#ffc000', '#4472c4', '#70ad47']),
                 ('OfficeClassic6', ['#4f81bd', '#c0504d', '#9bbb59', '#8064a2', '#4bacc6', '#f79646']),
                 ('Opulent6', ['#b83d68', '#ac66bb', '#de6c36', '#f9b639', '#cf6da4', '#fa8d3d']),
                 ('Orange6', ['#e48312', '#bd582c', '#865640', '#9b8357', '#c2bc80', '#94a088']),
                 ('OrangeRed6', ['#d34817', '#9b2d1f', '#a28e6a', '#956251', '#918485', '#855d5d']),
                 ('Orbit6', ['#f2d908', '#9de61e', '#0d8be6', '#c61b1b', '#e26f08', '#8d35d1']),
                 ('Organic6', ['#83992a', '#3c9770', '#44709d', '#a23c33', '#d97828', '#deb340']),
                 ('Oriel6', ['#fe8637', '#7598d9', '#b32c16', '#f5cd2d', '#aebad5', '#777c84']),
                 ('Origin6', ['#727ca3', '#9fb8cd', '#d2da7a', '#fada7a', '#b88472', '#8e736a']),
                 ('Paper6', ['#a5b592', '#f3a447', '#e7bc29', '#d092a7', '#9c85c0', '#809ec2']),
                 ('Parallax6', ['#30acec', '#80c34f', '#e29d3e', '#d64a3b', '#d64787', '#a666e1']),
                 ('Parcel6', ['#f6a21d', '#9bafb5', '#c96731', '#9ca383', '#87795d', '#a0988c']),
                 ('Perception6', ['#a2c816', '#e07602', '#e4c402', '#7dc1ef', '#21449b', '#a2b170']),
                 ('Perspective6', ['#838d9b', '#d2610c', '#80716a', '#94147c', '#5d5ad2', '#6f6c7d']),
                 ('Pixel6', ['#ff7f01', '#f1b015', '#fbec85', '#d2c2f1', '#da5af4', '#9d09d1']),
                 ('Plaza6', ['#990000', '#580101', '#e94a00', '#eb8f00', '#a4a4a4', '#666666']),
                 ('Precedent6', ['#993232', '#9b6c34', '#736c5d', '#c9972b', '#c95f2b', '#8f7a05']),
                 ('Pushpin6', ['#fda023', '#aa2b1e', '#71685c', '#64a73b', '#eb5605', '#b9ca1a']),
                 ('Quotable6', ['#00c6bb', '#6feba0', '#b6df5e', '#efb251', '#ef755f', '#ed515c']),
                 ('Red6', ['#a5300f', '#d55816', '#e19825', '#b19c7d', '#7f5f52', '#b27d49']),
                 ('RedOrange6', ['#e84c22', '#ffbd47', '#b64926', '#ff8427', '#cc9900', '#b22600']),
                 ('RedViolet6', ['#e32d91', '#c830cc', '#4ea6dc', '#4775e7', '#8971e1', '#d54773']),
                 ('Retrospect6', ['#e48312', '#bd582c', '#865640', '#9b8357', '#c2bc80', '#94a088']),
                 ('Revolution6', ['#0c5986', '#ddf53d', '#508709', '#bf5e00', '#9c0001', '#660075']),
                 ('Saddle6', ['#c6b178', '#9c5b14', '#71b2bc', '#78aa5d', '#867099', '#4c6f75']),
                 ('Savon6', ['#1cade4', '#2683c6', '#27ced7', '#42ba97', '#3e8853', '#62a39f']),
                 ('Sketchbook6', ['#a63212', '#e68230', '#9bb05e', '#6b9bc7', '#4e66b2', '#8976ac']),
                 ('Sky6', ['#073779', '#8fd9fb', '#ffcc00', '#eb6615', '#c76402', '#b523b4']),
                 ('Slate6', ['#bc451b', '#d3ba68', '#bb8640', '#ad9277', '#a55a43', '#ad9d7b']),
                 ('Slice6', ['#052f61', '#a50e82', '#14967c', '#6a9e1f', '#e87d37', '#c62324']),
                 ('Slipstream6', ['#4e67c8', '#5eccf3', '#a7ea52', '#5dceaf', '#ff8021', '#f14124']),
                 ('SOHO6', ['#61625e', '#964d2c', '#66553e', '#848058', '#afa14b', '#ad7d4d']),
                 ('Solstice6', ['#3891a7', '#feb80a', '#c32d2e', '#84aa33', '#964305', '#475a8d']),
                 ('Spectrum6', ['#990000', '#ff6600', '#ffba00', '#99cc00', '#528a02', '#333333']),
                 ('Story6', ['#1d86cd', '#732e9a', '#b50b1b', '#e8950e', '#55992b', '#2c9c89']),
                 ('Studio6', ['#f7901e', '#fec60b', '#9fe62f', '#4ea5d1', '#1c4596', '#542d90']),
                 ('Summer6', ['#51a6c2', '#51c2a9', '#7ec251', '#e1dc53', '#b54721', '#a16bb1']),
                 ('Technic6', ['#6ea0b0', '#ccaf0a', '#8d89a4', '#748560', '#9e9273', '#7e848d']),
                 ('Thatch6', ['#759aa5', '#cfc60d', '#99987f', '#90ac97', '#ffad1c', '#b9ab6f']),
                 ('Tradition6', ['#6b4a0b', '#790a14', '#908342', '#423e5c', '#641345', '#748a2f']),
                 ('Travelogue6', ['#b74d21', '#a32323', '#4576a3', '#615d9a', '#67924b', '#bf7b1b']),
                 ('Trek6', ['#f0a22e', '#a5644e', '#b58b80', '#c3986d', '#a19574', '#c17529']),
                 ('Twilight6', ['#e8bc4a', '#83c1c6', '#e78d35', '#909ce1', '#839c41', '#cc5439']),
                 ('Urban6', ['#53548a', '#438086', '#a04da3', '#c4652d', '#8b5d3d', '#5c92b5']),
                 ('UrbanPop6', ['#86ce24', '#00a2e6', '#fac810', '#7d8f8c', '#d06b20', '#958b8b']),
                 ('VaporTrail6', ['#df2e28', '#fe801a', '#e9bf35', '#81bb42', '#32c7a9', '#4a9bdc']),
                 ('Venture6', ['#9eb060', '#d09a08', '#f2ec86', '#824f1c', '#511818', '#553876']),
                 ('Verve6', ['#ff388c', '#e40059', '#9c007f', '#68007f', '#005bd3', '#00349e']),
                 ('View6', ['#6f6f74', '#92a9b9', '#a7b789', '#b9a489', '#8d6374', '#9b7362']),
                 ('Violet6', ['#ad84c6', '#8784c7', '#5d739a', '#6997af', '#84acb6', '#6f8183']),
                 ('VioletII6', ['#92278f', '#9b57d3', '#755dd9', '#665eb8', '#45a5ed', '#5982db']),
                 ('Waveform6', ['#31b6fd', '#4584d3', '#5bd078', '#a5d028', '#f5c040', '#05e0db']),
                 ('Wisp6', ['#a53010', '#de7e18', '#9f8351', '#728653', '#92aa4c', '#6aac91']),
                 ('WoodType6', ['#d34817', '#9b2d1f', '#a28e6a', '#956251', '#918485', '#855d5d']),
                 ('Yellow6', ['#ffca08', '#f8931d', '#ce8d3e', '#ec7016', '#e64823', '#9c6a6a']),
                 ('YellowOrange6', ['#f0a22e', '#a5644e', '#b58b80', '#c3986d', '#a19574', '#c17529']),
                 ('Tableau10',
                  ['#4E79A7', '#F28E2B', '#E15759', '#76B7B2', '#59A14F', '#EDC948', '#B07AA1', '#FF9DA7', '#9C755F',
                   '#BAB0AC']),
                 ('Tableau20',
                  ['#4E79A7', '#A0CBE8', '#F28E2B', '#FFBE7D', '#59A14F', '#8CD17D', '#B6992D', '#F1CE63', '#499894',
                   '#86BCB6',
                   '#E15759', '#FF9D9A', '#79706E', '#BAB0AC', '#D37295', '#FABFD2', '#B07AA1', '#D4A6C8', '#9D7660',
                   '#D7B5A6']),
                 ('ColorBlind10',
                  ['#1170aa', '#fc7d0b', '#a3acb9', '#57606c', '#5fa2ce', '#c85200', '#7b848f', '#a3cce9', '#ffbc79',
                   '#c8d0d9']),
                 ('SeattleGrays5', ['#767f8b', '#b3b7b8', '#5c6068', '#d3d3d3', '#989ca3']),
                 ('Traffic9',
                  ['#b60a1c', '#e39802', '#309143', '#e03531', '#f0bd27', '#51b364', '#ff684c', '#ffda66', '#8ace7e']),
                 ('MillerStone11',
                  ['#4f6980', '#849db1', '#a2ceaa', '#638b66', '#bfbb60', '#f47942', '#fbb04e', '#b66353', '#d7ce9f',
                   '#b9aa97',
                   '#7e756d']),
                 ('SuperfishelStone10',
                  ['#6388b4', '#ffae34', '#ef6f6a', '#8cc2ca', '#55ad89', '#c3bc3f', '#bb7693', '#baa094', '#a9b5ae',
                   '#767676']),
                 ('NurielStone9',
                  ['#8175aa', '#6fb899', '#31a1b3', '#ccb22b', '#a39fc9', '#94d0c0', '#959c9e', '#027b8e', '#9f8f12']),
                 ('JewelBright9',
                  ['#eb1e2c', '#fd6f30', '#f9a729', '#f9d23c', '#5fbb68', '#64cdcc', '#91dcea', '#a4a4d5', '#bbc9e5']),
                 ('Summer8', ['#bfb202', '#b9ca5d', '#cf3e53', '#f1788d', '#00a2b3', '#97cfd0', '#f3a546', '#f7c480']),
                 ('Winter10',
                  ['#90728f', '#b9a0b4', '#9d983d', '#cecb76', '#e15759', '#ff9888', '#6b6b6b', '#bab2ae', '#aa8780',
                   '#dab6af']),
                 ('GreenOrangeTeal12',
                  ['#4e9f50', '#87d180', '#ef8a0c', '#fcc66d', '#3ca8bc', '#98d9e4', '#94a323', '#c3ce3d', '#a08400',
                   '#f7d42a',
                   '#26897e', '#8dbfa8']),
                 ('RedBlueBrown12',
                  ['#466f9d', '#91b3d7', '#ed444a', '#feb5a2', '#9d7660', '#d7b5a6', '#3896c4', '#a0d4ee', '#ba7e45',
                   '#39b87f',
                   '#c8133b', '#ea8783']),
                 ('PurplePinkGray12',
                  ['#8074a8', '#c6c1f0', '#c46487', '#ffbed1', '#9c9290', '#c5bfbe', '#9b93c9', '#ddb5d5', '#7c7270',
                   '#f498b6',
                   '#b173a0', '#c799bc']),
                 ('HueCircle19',
                  ['#1ba3c6', '#2cb5c0', '#30bcad', '#21B087', '#33a65c', '#57a337', '#a2b627', '#d5bb21', '#f8b620',
                   '#f89217',
                   '#f06719', '#e03426', '#f64971', '#fc719e', '#eb73b3', '#ce69be', '#a26dc2', '#7873c0', '#4f7cba']),
                 ('OrangeBlue7', ['#9e3d22', '#d45b21', '#f69035', '#d9d5c9', '#77acd3', '#4f81af', '#2b5c8a']),
                 ('RedGreen7', ['#a3123a', '#e33f43', '#f8816b', '#ced7c3', '#73ba67', '#44914e', '#24693d']),
                 ('GreenBlue7', ['#24693d', '#45934d', '#75bc69', '#c9dad2', '#77a9cf', '#4e7fab', '#2a5783']),
                 ('RedBlue7', ['#a90c38', '#e03b42', '#f87f69', '#dfd4d1', '#7eaed3', '#5383af', '#2e5a87']),
                 ('RedBlack7', ['#ae123a', '#e33e43', '#f8816b', '#d9d9d9', '#a0a7a8', '#707c83', '#49525e']),
                 ('GoldPurple7', ['#ad9024', '#c1a33b', '#d4b95e', '#e3d8cf', '#d4a3c3', '#c189b0', '#ac7299']),
                 ('RedGreenGold7', ['#be2a3e', '#e25f48', '#f88f4d', '#f4d166', '#90b960', '#4b9b5f', '#22763f']),
                 ('SunsetSunrise7', ['#33608c', '#9768a5', '#e7718a', '#f6ba57', '#ed7846', '#d54c45', '#b81840']),
                 ('OrangeBlueWhite7', ['#9e3d22', '#e36621', '#fcad52', '#ffffff', '#95c5e1', '#5b8fbc', '#2b5c8a']),
                 ('RedGreenWhite7', ['#ae123a', '#ee574d', '#fdac9e', '#ffffff', '#91d183', '#539e52', '#24693d']),
                 ('GreenBlueWhite7', ['#24693d', '#529c51', '#8fd180', '#ffffff', '#95c1dd', '#598ab5', '#2a5783']),
                 ('RedBlueWhite7', ['#a90c38', '#ec534b', '#feaa9a', '#ffffff', '#9ac4e1', '#5c8db8', '#2e5a87']),
                 ('RedBlackWhite7', ['#ae123a', '#ee574d', '#fdac9d', '#ffffff', '#bdc0bf', '#7d888d', '#49525e']),
                 ('OrangeBlueLight7', ['#ffcc9e', '#f9d4b6', '#f0dccd', '#e5e5e5', '#dae1ea', '#cfdcef', '#c4d8f3']),
                 ('Temperature7', ['#529985', '#6c9e6e', '#99b059', '#dbcf47', '#ebc24b', '#e3a14f', '#c26b51']),
                 ('BlueGreen7', ['#feffd9', '#f2fabf', '#dff3b2', '#c4eab1', '#94d6b7', '#69c5be', '#41b7c4']),
                 ('BlueLight7', ['#e5e5e5', '#e0e3e8', '#dbe1ea', '#d5dfec', '#d0dcef', '#cadaf1', '#c4d8f3']),
                 ('OrangeLight7', ['#e5e5e5', '#ebe1d9', '#f0ddcd', '#f5d9c2', '#f9d4b6', '#fdd0aa', '#ffcc9e']),
                 ('Blue20',
                  ['#b9ddf1', '#afd6ed', '#a5cfe9', '#9bc7e4', '#92c0df', '#89b8da', '#80b0d5', '#79aacf', '#72a3c9',
                   '#6a9bc3',
                   '#6394be', '#5b8cb8', '#5485b2', '#4e7fac', '#4878a6', '#437a9f', '#3d6a98', '#376491', '#305d8a',
                   '#2a5783']),
                 ('Orange20',
                  ['#ffc685', '#fcbe75', '#f9b665', '#f7ae54', '#f5a645', '#f59c3c', '#f49234', '#f2882d', '#f07e27',
                   '#ee7422',
                   '#e96b20', '#e36420', '#db5e20', '#d25921', '#ca5422', '#c14f22', '#b84b23', '#af4623', '#a64122',
                   '#9e3d22']),
                 ('Green20',
                  ['#b3e0a6', '#a5db96', '#98d687', '#8ed07f', '#85ca77', '#7dc370', '#75bc69', '#6eb663', '#67af5c',
                   '#61a956',
                   '#59a253', '#519c51', '#49964f', '#428f4d', '#398949', '#308344', '#2b7c40', '#27763d', '#256f3d',
                   '#24693d']),
                 ('Red20',
                  ['#ffbeb2', '#feb4a6', '#fdab9b', '#fca290', '#fb9984', '#fa8f79', '#f9856e', '#f77b66', '#f5715d',
                   '#f36754',
                   '#f05c4d', '#ec5049', '#e74545', '#e13b42', '#da323f', '#d3293d', '#ca223c', '#c11a3b', '#b8163a',
                   '#ae123a']),
                 ('Purple20',
                  ['#eec9e5', '#eac1df', '#e6b9d9', '#e0b2d2', '#daabcb', '#d5a4c4', '#cf9dbe', '#ca96b8', '#c48fb2',
                   '#be89ac',
                   '#b882a6', '#b27ba1', '#aa759d', '#a27099', '#9a6a96', '#926591', '#8c5f86', '#865986', '#81537f',
                   '#7c4d79']),
                 ('Brown20',
                  ['#eedbbd', '#ecd2ad', '#ebc994', '#eac085', '#e8b777', '#e5ae6c', '#e2a562', '#de9d5a', '#d99455',
                   '#d38c54',
                   '#ce8451', '#c9784d', '#c47247', '#c16941', '#bd6036', '#b85636', '#b34d34', '#ad4433', '#a63d32',
                   '#9f3632']),
                 ('Gray20',
                  ['#d5d5d5', '#cdcecd', '#c5c7c6', '#bcbfbe', '#b4b7b7', '#acb0b1', '#a4a9ab', '#9ca3a4', '#939c9e',
                   '#8b9598',
                   '#848e93', '#7c878d', '#758087', '#6e7a81', '#67737c', '#616c77', '#5b6570', '#555f6a', '#4f5864',
                   '#49525e']),
                 ('GrayWarm20',
                  ['#dcd4d0', '#d4ccc8', '#cdc4c0', '#c5bdb9', '#beb6b2', '#b7afab', '#b0a7a4', '#a9a09d', '#a29996',
                   '#9b938f',
                   '#948c88', '#8d8481', '#867e7b', '#807774', '#79706e', '#736967', '#6c6260', '#665c51', '#5f5654',
                   '#59504e']),
                 ('BlueTeal20',
                  ['#bce4d8', '#aedcd5', '#a1d5d2', '#95cecf', '#89c8cc', '#7ec1ca', '#72bac6', '#66b2c2', '#59acbe',
                   '#4ba5ba',
                   '#419eb6', '#3b96b2', '#358ead', '#3586a7', '#347ea1', '#32779b', '#316f96', '#2f6790', '#2d608a',
                   '#2c5985']),
                 ('OrangeGold20',
                  ['#f4d166', '#f6c760', '#f8bc58', '#f8b252', '#f7a84a', '#f69e41', '#f49538', '#f38b2f', '#f28026',
                   '#f0751e',
                   '#eb6c1c', '#e4641e', '#de5d1f', '#d75521', '#cf4f22', '#c64a22', '#bc4623', '#b24223', '#a83e24',
                   '#9e3a26']),
                 ('GreenGold20',
                  ['#f4d166', '#e3cd62', '#d3c95f', '#c3c55d', '#b2c25b', '#a3bd5a', '#93b958', '#84b457', '#76af56',
                   '#67a956',
                   '#5aa355', '#4f9e53', '#479751', '#40914f', '#3a8a4d', '#34844a', '#2d7d45', '#257740', '#1c713b',
                   '#146c36']),
                 ('RedGold21',
                  ['#f4d166', '#f5c75f', '#f6bc58', '#f7b254', '#f9a750', '#fa9d4f', '#fa9d4f', '#fb934d', '#f7894b',
                   '#f47f4a',
                   '#f0774a', '#eb6349', '#e66549', '#e15c48', '#dc5447', '#d64c45', '#d04344', '#ca3a42', '#c43141',
                   '#bd273f', '#b71d3e']),
                 ('Classic10',
                  ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22',
                   '#17becf']),
                 ('ClassicMedium10',
                  ['#729ece', '#ff9e4a', '#67bf5c', '#ed665d', '#ad8bc9', '#a8786e', '#ed97ca', '#a2a2a2', '#cdcc5d',
                   '#6dccda']),
                 ('ClassicLight10',
                  ['#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5', '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d',
                   '#9edae5']),
                 ('Classic20',
                  ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd',
                   '#c5b0d5',
                   '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf',
                   '#9edae5']),
                 ('ClassicGray5', ['#60636a', '#a5acaf', '#414451', '#8f8782', '#cfcfcf']),
                 ('ClassicColorBlind10',
                  ['#006ba4', '#ff800e', '#ababab', '#595959', '#5f9ed1', '#c85200', '#898989', '#a2c8ec', '#ffbc79',
                   '#cfcfcf']),
                 ('ClassicTrafficLight9',
                  ['#b10318', '#dba13a', '#309343', '#d82526', '#ffc156', '#69b764', '#f26c64', '#ffdd71', '#9fcd99']),
                 ('ClassicPurpleGray6', ['#7b66d2', '#dc5fbd', '#94917b', '#995688', '#d098ee', '#d7d5c5']),
                 ('ClassicPurpleGray12',
                  ['#7b66d2', '#a699e8', '#dc5fbd', '#ffc0da', '#5f5a41', '#b4b19b', '#995688', '#d898ba', '#ab6ad5',
                   '#d098ee',
                   '#8b7c6e', '#dbd4c5']),
                 ('ClassicGreenOrange6', ['#32a251', '#ff7f0f', '#3cb7cc', '#ffd94a', '#39737c', '#b85a0d']),
                 ('ClassicGreenOrange12',
                  ['#32a251', '#acd98d', '#ff7f0f', '#ffb977', '#3cb7cc', '#98d9e4', '#b85a0d', '#ffd94a', '#39737c',
                   '#86b4a9',
                   '#82853b', '#ccc94d']),
                 ('ClassicBlueRed6', ['#2c69b0', '#f02720', '#ac613c', '#6ba3d6', '#ea6b73', '#e9c39b']),
                 ('ClassicBlueRed12',
                  ['#2c69b0', '#b5c8e2', '#f02720', '#ffb6b0', '#ac613c', '#e9c39b', '#6ba3d6', '#b5dffd', '#ac8763',
                   '#ddc9b4',
                   '#bd0a36', '#f4737a']),
                 ('ClassicCyclic13',
                  ['#1f83b4', '#12a2a8', '#2ca030', '#78a641', '#bcbd22', '#ffbf50', '#ffaa0e', '#ff7f0e', '#d63a3a',
                   '#c7519c',
                   '#ba43b4', '#8a60b0', '#6f63bb']),
                 ('ClassicGreen7', ['#bccfb4', '#94bb83', '#69a761', '#339444', '#27823b', '#1a7232', '#09622a']),
                 ('ClassicGray13',
                  ['#c3c3c3', '#b2b2b2', '#a2a2a2', '#929292', '#838383', '#747474', '#666666', '#585858', '#4b4b4b',
                   '#3f3f3f',
                   '#333333', '#282828', '#1e1e1e']),
                 ('ClassicBlue7', ['#b4d4da', '#7bc8e2', '#67add4', '#3a87b7', '#1c73b1', '#1c5998', '#26456e']),
                 ('ClassicRed9',
                  ['#eac0bd', '#f89a90', '#f57667', '#e35745', '#d8392c', '#cf1719', '#c21417', '#b10c1d', '#9c0824']),
                 ('ClassicOrange7', ['#f0c294', '#fdab67', '#fd8938', '#f06511', '#d74401', '#a33202', '#7b3014']),
                 ('ClassicAreaRed11',
                  ['#f5cac7', '#fbb3ab', '#fd9c8f', '#fe8b7a', '#fd7864', '#f46b55', '#ea5e45', '#e04e35', '#d43e25',
                   '#c92b14',
                   '#bd1100']),
                 ('ClassicAreaGreen11',
                  ['#dbe8b4', '#c3e394', '#acdc7a', '#9ad26d', '#8ac765', '#7abc5f', '#6cae59', '#60a24d', '#569735',
                   '#4a8c1c',
                   '#3c8200']),
                 ('ClassicAreaBrown11',
                  ['#f3e0c2', '#f6d29c', '#f7c577', '#f0b763', '#e4aa63', '#d89c63', '#cc8f63', '#c08262', '#bb7359',
                   '#bb6348',
                   '#bb5137']),
                 ('ClassicRedGreen11',
                  ['#9c0824', '#bd1316', '#d11719', '#df513f', '#fc8375', '#cacaca', '#a2c18f', '#69a761', '#2f8e41',
                   '#1e7735',
                   '#09622a']),
                 ('ClassicRedBlue11',
                  ['#9c0824', '#bd1316', '#d11719', '#df513f', '#fc8375', '#cacaca', '#67add4', '#3a87b7', '#1c73b1',
                   '#1c5998',
                   '#26456e']),
                 ('ClassicRedBlack11',
                  ['#9c0824', '#bd1316', '#d11719', '#df513f', '#fc8375', '#cacaca', '#9b9b9b', '#777777', '#565656',
                   '#383838',
                   '#1e1e1e']),
                 ('ClassicAreaRedGreen21',
                  ['#bd1100', '#c82912', '#d23a21', '#dc4930', '#e6583e', '#ef654d', '#f7705b', '#fd7e6b', '#fe8e7e',
                   '#fca294',
                   '#e9dabe', '#c7e298', '#b1de7f', '#a0d571', '#90cb68', '#82c162', '#75b65d', '#69aa56', '#5ea049',
                   '#559633', '#4a8c1c']),
                 ('ClassicOrangeBlue13',
                  ['#7b3014', '#a33202', '#d74401', '#f06511', '#fd8938', '#fdab67', '#cacaca', '#7bc8e2', '#67add4',
                   '#3a87b7',
                   '#1c73b1', '#1c5998', '#26456e']),
                 ('ClassicGreenBlue11',
                  ['#09622a', '#1e7735', '#2f8e41', '#69a761', '#a2c18f', '#cacaca', '#67add4', '#3a87b7', '#1c73b1',
                   '#1c5998',
                   '#26456e']),
                 ('ClassicRedWhiteGreen11',
                  ['#9c0824', '#b41f27', '#cc312b', '#e86753', '#fcb4a5', '#ffffff', '#b9d7b7', '#74af72', '#428f49',
                   '#297839',
                   '#09622a']),
                 ('ClassicRedWhiteBlack11',
                  ['#9c0824', '#b41f27', '#cc312b', '#e86753', '#fcb4a5', '#ffffff', '#bfbfbf', '#838383', '#575757',
                   '#393939',
                   '#1e1e1e']),
                 ('ClassicOrangeWhiteBlue11',
                  ['#7b3014', '#a84415', '#d85a13', '#fb8547', '#ffc2a1', '#ffffff', '#b7cde2', '#6a9ec5', '#3679a8',
                   '#2e5f8a',
                   '#26456e']),
                 ('ClassicRedWhiteBlackLight10',
                  ['#ffc2c5', '#ffd1d3', '#ffe0e1', '#fff0f0', '#ffffff', '#f3f3f3', '#e8e8e8', '#dddddd', '#d1d1d1',
                   '#c6c6c6']),
                 ('ClassicOrangeWhiteBlueLight11',
                  ['#ffcc9e', '#ffd6b1', '#ffe0c5', '#ffead8', '#fff5eb', '#ffffff', '#f3f7fd', '#e8effa', '#dce8f8',
                   '#d0e0f6',
                   '#c4d8f3']),
                 ('ClassicRedWhiteGreenLight11',
                  ['#ffb2b6', '#ffc2c5', '#ffd1d3', '#ffe0e1', '#fff0f0', '#ffffff', '#f1faed', '#e3f5db', '#d5f0ca',
                   '#c6ebb8',
                   '#b7e6a7']),
                 ('ClassicRedGreenLight11',
                  ['#ffb2b6', '#fcbdc0', '#f8c7c9', '#f2d1d2', '#ecdbdc', '#e5e5e5', '#dde6d9', '#d4e6cc', '#cae6c0',
                   '#c1e6b4',
                   '#b7e6a7'])]


class TSDashboard(models.Model):
    _name = "ts.dashboard"
    _description = "Dashboard"

    name = fields.Char("name", required=True)
    web_color = fields.Char("Color", help="Choose your color")
    type = fields.Selection([('tile', 'Tile'),
                             ('bar', 'Bar Chart'),
                             ('pie', 'Pie Chart'),
                             # ('polarArea', 'Polar Area Chart'),
                             ('line', 'Line Chart'),
                             ('list', 'List View')], string="Type", required=True)

    active = fields.Boolean(default=True)
    pie_type = fields.Selection([('doughnut', 'Doughnut'),
                                 ('pie', 'Pie')], string="Pie Type", default='pie', copy=False)
    bar_type = fields.Selection([('bar', 'Vertical Bar'),
                                 ('horizontalBar', 'Horizontal Bar')], string="Bar Type", default='bar')
    is_stacked_bar = fields.Boolean("Is Stacked Bar Chart", default=False, copy=False)
    is_semi_circle_bar = fields.Boolean("Is Semi Circle Chart", default=False, copy=False)
    operation_type = fields.Selection([('Sum', 'Sum'),
                                       ('Avg', 'Average'),
                                       ('Count', 'Count')], string="Operation Type")
    color = fields.Selection([('blue', 'Blue'),
                              ('green', 'Green'),
                              ('yellow', 'Yellow'),
                              ('pink', 'Pink'),
                              ('mint', 'Mint')], default='blue', string="Color")
    chart_colors = fields.Selection(CHART_COLORS, default='tableau.HueCircle19', string="Chart Color")
    fa_icon = fields.Char("Icon", help="Icons used in Dashboard.")
    dashboard_model_id = fields.Many2one('ir.model', string='Model', required=True,
                                         help="The model this field belongs to")
    dashboard_model_name = fields.Char(related='dashboard_model_id.model', string='Model Name', readonly=True,
                                       related_sudo=True)
    dashboard_domain = fields.Char(string='Model Domain', default=[])
    measure_field_id = fields.Many2one('ir.model.fields', string='Measure Field',
                                       domain="[('model_id','=',dashboard_model_id),('store','=',True),'|','|',('ttype','=','integer'),('ttype','=','float'),('ttype','=','monetary')]", copy=True)
    date_filter_field_id = fields.Many2one('ir.model.fields', string='Date Filter Field',
                                           domain="[('model_id','=',dashboard_model_id),('store','=',True),'|',('ttype','=','date'),('ttype','=','datetime')]", copy=True)
    show_currency_symbol = fields.Boolean("Show Currency Symbol?", default=False, copy=False)

    # Graph Fields
    groupby_field_id = fields.Many2one('ir.model.fields', string='Group By',
                                       domain="[('model_id','=',dashboard_model_id),('store','=',True),'|','|','|',('ttype','=','many2one'),('ttype','=','selection'),('ttype','=','date'),('ttype','=','datetime')]",
                                       copy=True)

    date_groupby_field_id = fields.Many2one('ir.model.fields', string='Group by Date',
                                            domain="[('model_id','=',dashboard_model_id),('store','=',True),'|',('ttype','=','date'),('ttype','=','datetime')]",
                                            copy=True)
    date_selection = fields.Selection([
        ('today', 'Today'),
        ('this_week', 'This Week'),
        ('this_month', 'This Month'),
        ('this_year', 'This Year'),
        ('yesterday', 'Yesterday'),
        ('last_week', 'Last Week'),
        ('last_month', 'Last Month'),
        ('last_year', 'Last Year'),
        ('tomorrow', 'Tomorrow'),
        ('next_week', 'Next Week'),
        ('next_month', 'Next Month'),
        ('next_year', 'Next Year'),
        ('c_range', 'Custom Range'),
    ], string='Date Filter Selection', help="This date is used in Group by for some Graphs.")
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')

    # Save Position
    height = fields.Integer("Height", copy=False, default=0)
    width = fields.Integer("Width", copy=False, default=0)
    x = fields.Integer("X-Axis", copy=False, default=0)
    y = fields.Integer("Y-Axis", copy=False, default=0)

    set_interval = fields.Selection([
        (10000, '10 Seconds'),
        (20000, '20 Seconds'),
        (30000, '30 Seconds'),
        (40000, '40 Seconds'),
        (60000, '1 minute'),
        (120000, '2 minutes'),
        (180000, '3 minutes'),
        (300000, '5 minutes'),
        (600000, '10 minutes'),
        (1200000, '20 minutes'),
    ], string="Data Update Time", help="Update dashboard data at certain second or minutes.")
    list_type = fields.Selection([('non_group', 'Non-Grouping'),('group', 'Grouping')], default='non_group')
    list_view_fields = fields.Many2many('ir.model.fields', 'dashboard_list_field_rel', 'list_field_id', 'field_id',
                                           domain="[('model_id','=',dashboard_model_id),('store','=',True),"
                                                  "('ttype','!=','one2many'),('ttype','!=','many2many'),('ttype','!=','binary')]",
                                           string="List View Columns")
    list_view_groupby_fields = fields.Many2many('ir.model.fields', 'dashboard_list_groupby_field_rel', 'list_field_id', 'field_id',
                                        domain="[('model_id','=',dashboard_model_id),('name','!=','id'),('store','=',True),'|','|',('ttype','=','integer'),"
                                               "('ttype','=','monetary'),('ttype','=','float')]",
                                        string="List View Columns")
    limit_record_count = fields.Integer("Limit Record Count")
    sorting_field = fields.Many2one('ir.model.fields', string="Sorting Field",
                                    domain="[('model_id','=',dashboard_model_id),('name','!=','id'),('store','=',True),('ttype','!=','one2many'),('ttype','!=','many2one'),('ttype','!=','binary')]")
    sorting_order = fields.Selection([('asc', 'Ascending'), ('desc', 'Descending')], string="Sorting Order")
    list_themes = fields.Char(default="#333333", string="List Themes")

    board_config_id = fields.Many2one('ts.board.config',
                                      default=lambda self: self._context['board_id'] if 'board_id' in self._context else False)
    # Chart Preview in Form View
    chart_preview = fields.Char("Preview", default="Chart Preview")
    chart_data = fields.Char("Chart Data Used for Form Preview", compute='get_chart_data_form_preview')

    @api.model
    def action_dashboard_redirect(self):
        if self.env.user.has_group('ts_dashboard.ts_dashboard_group_manager'):
            return self.env.ref('ts_dashboard.backend_ts_dashboard').read()[0]
        return self.env.ref('ts_dashboard.action_dashboard').read()[0]

    @api.multi
    def save_grid_position(self, grid_position, interval_value=False):
        for grid in grid_position:
            self.browse(grid['id']).write(
                {'x': grid['x'], 'y': grid['y'], 'width': grid['width'], 'height': grid['height']})
        if interval_value != False:
            self.env['ir.config_parameter'].sudo().set_param('refresh_interval', interval_value)
        return True

    @api.onchange('chart_colors')
    def onchange_chart_colors(self):
        hexcodes = dict(COLOR_HEXCODE)[self.chart_colors.split('.')[1]]
        self.web_color = ", ".join(hexcodes)

    @api.onchange('dashboard_model_id')
    def onchange_dashboard_model_id(self):
        self.measure_field_id = False
        self.date_filter_field_id = False
        self.groupby_field_id = False
        self.sorting_field = False
        self.list_view_fields = False
        self.list_view_groupby_fields = False
        self.dashboard_domain = []

    @api.onchange('list_type')
    def onchange_list_type(self):
        self.list_view_groupby_fields = False
        self.list_view_fields = False

    def get_date_range(self):
        date_selection = self.date_selection
        today = datetime.date.today()
        if date_selection == 'today':
            start_date = end_date = today
        elif date_selection == 'this_week':
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)
        elif date_selection == 'this_month':
            start_date = today.replace(day=1)
            end_date = today
        elif date_selection == 'this_year':
            start_date = today.replace(month=1, day=1)
            end_date = today
        elif date_selection == 'yesterday':
            start_date = end_date = today - datetime.timedelta(days=1)
        elif date_selection == 'last_week':
            start_date = today + datetime.timedelta(-today.weekday(), weeks=-1)
            end_date = today + datetime.timedelta(-today.weekday() - 1)
        elif date_selection == 'last_month':
            this_month_start = today.replace(day=1)
            end_date = this_month_start - datetime.timedelta(days=1)
            start_date = end_date.replace(day=1)
        elif date_selection == 'last_year':
            start_date = today.replace(month=1, day=1, year=today.year - 1)
            end_date = today.replace(month=1, day=1, year=today.year) - datetime.timedelta(days=1)
        elif date_selection == 'tomorrow':
            start_date = end_date = datetime.date.today() + datetime.timedelta(days=1)
        elif date_selection == 'next_week':
            start_date = today + datetime.timedelta(-today.weekday(), weeks=1)
            end_date = start_date + timedelta(days=6)
        elif date_selection == 'next_month':
            start_date = (today + relativedelta.relativedelta(months=1)).replace(day=1)
            end_date = (today + relativedelta.relativedelta(months=2)).replace(day=1) - datetime.timedelta(days=1)
        elif date_selection == 'next_year':
            start_date = (today + relativedelta.relativedelta(years=1)).replace(day=1, month=1)
            end_date = (today + relativedelta.relativedelta(years=2)).replace(day=1, month=1).replace(
                day=1) - datetime.timedelta(days=1)
        elif date_selection == 'c_range':
            start_date = fields.Date.from_string(self.start_date)
            end_date = fields.Date.from_string(self.end_date)
        return start_date, end_date

    def prepare_data_for_tile(self, dashboard, filtered_ids, where_condition, dashboard_data=False):
        res = 0
        model_obj = self.env[dashboard['dashboard_model_name']]
        dashboard_id = self.env['ts.dashboard'].browse(dashboard['id']).sudo()
        if filtered_ids and dashboard['operation_type'] and dashboard_id.measure_field_id:
            query = '''SELECT %s(%s) FROM %s %s''' % (
                (dashboard['operation_type']), dashboard_id.measure_field_id.name,
                (model_obj._name).replace('.', '_'), where_condition)
            if dashboard['limit_record_count'] > 0:
                query = query + ' limit {}'.format(dashboard['limit_record_count'])
            self._cr.execute(query)
            res = self._cr.fetchone()
        if isinstance(dashboard_data, dict):
            if dashboard['show_currency_symbol'] and self.env.user.company_id.currency_id:
                dashboard_data.update({'currency_id': self.env.user.company_id.currency_id.id})
            dashboard_data.update({'display_result': res[0] if res else 0})
        else:
            if dashboard['show_currency_symbol'] and self.env.user.company_id.currency_id:
                dashboard.update({'currency_id': self.env.user.company_id.currency_id.id})
            dashboard.update({'display_result': res[0] if res else 0})
        return True

    def prepare_data_for_tile_form_renderer(self, dashboard, filtered_ids, where_condition, dashboard_data=False):
        res = 0
        model_obj = self.env[dashboard['dashboard_model_name']]
        if filtered_ids and dashboard['operation_type'] and dashboard.measure_field_id:
            query = '''SELECT %s(%s) FROM %s %s''' % (
                (dashboard['operation_type']), dashboard.measure_field_id.name,
                (model_obj._name).replace('.', '_'), where_condition)
            if dashboard['limit_record_count'] > 0:
                query = query + ' limit {}'.format(dashboard['limit_record_count'])
            self._cr.execute(query)
            res = self._cr.fetchone()
        if isinstance(dashboard_data, dict):
            if dashboard['show_currency_symbol'] and self.env.user.company_id.currency_id:
                dashboard_data.update({'currency_id': self.env.user.company_id.currency_id.id})
            dashboard_data.update({'display_result': res[0] if res else 0})
        else:
            if dashboard['show_currency_symbol'] and self.env.user.company_id.currency_id:
                dashboard.update({'currency_id': self.env.user.company_id.currency_id.id})
            dashboard.update({'display_result': res[0] if res else 0})
        return True

    def get_chart_data(self, groupby_field_id, dashboard, where_condition):
        model_obj = self.env[dashboard['dashboard_model_name']]
        query = """
                    SELECT
                       %s, %s (%s)
                    FROM
                       %s
                       %s
                    GROUP BY
                       %s;
                """ % (
            "{}::date".format(groupby_field_id.name) if groupby_field_id.ttype in ['datetime'] else groupby_field_id.name,
            dashboard['operation_type'], self.measure_field_id.name,
            (model_obj._name).replace('.', '_'), where_condition, "{}::date".format(groupby_field_id.name) if groupby_field_id.ttype in ['datetime'] else groupby_field_id.name)
        self._cr.execute(query)
        return self._cr.dictfetchall()

    def get_dashboard_data(self, dashboard_ids):
        def Remove(duplicate):
            final_list = []
            for num in duplicate:
                if num not in final_list:
                    final_list.append(num)
            return final_list
        dashboard_data = self.sudo().search_read([('id', 'in', dashboard_ids.ids)], [], order='')
        for dashboard in dashboard_data:
            if not dashboard.get('id', False) or not dashboard['dashboard_model_name']:
                continue
            date_domain = []
            dashboard_id = self.browse(dashboard['id']).sudo()
            groupby_field_id = dashboard_id.groupby_field_id
            is_relation_field = groupby_field_id.ttype == 'many2one'
            relation_field_obj = self.env[groupby_field_id.relation] if is_relation_field else False
            date_filter_field = dashboard_id.date_filter_field_id.name
            model_obj = self.env[dashboard['dashboard_model_name']]
            if dashboard_id.date_selection and date_filter_field:
                start_date, end_date = dashboard_id.get_date_range()
                date_domain = [(date_filter_field, '>=', fields.Date.to_string(start_date)),
                               (date_filter_field, '<=', fields.Date.to_string(end_date))]

            filtered_ids = model_obj.search(
                safe_eval(dashboard['dashboard_domain']) + date_domain)
            where_condition = ''
            if len(filtered_ids) == 1:
                where_condition = 'WHERE id = %s' % (filtered_ids.id)
            elif len(filtered_ids) > 1:
                where_condition = 'WHERE id in {}'.format(tuple(filtered_ids.ids))

            if dashboard_id.date_selection and date_filter_field and not where_condition:
                continue

            if dashboard['type'] == 'tile':
                self.prepare_data_for_tile(dashboard, filtered_ids, where_condition)

            elif dashboard['type'] in ['line', 'bar', 'pie', 'polarArea']:
                res = dashboard_id.get_chart_data(groupby_field_id, dashboard, where_condition)
                chart_data_list = []
                operation_type = dashboard_id.operation_type.lower()
                res = sorted([d for d in res if all(d.values())], key=lambda i: i[groupby_field_id.name])

                labels = [r[groupby_field_id.name].strftime("%D") if groupby_field_id.ttype in ['datetime','date'] else r[groupby_field_id.name] for r in res]
                if is_relation_field:
                    labels = [record.name for record in relation_field_obj.browse(labels)]

                if dashboard['type'] in ['pie', 'polarArea']:
                    chart_data_list.append({'data': [r[operation_type] for r in res]})
                else:
                    for record in res:
                        for label in labels:
                            label_name = relation_field_obj.browse(record.get(groupby_field_id.name)).name if is_relation_field else record.get(groupby_field_id.name).strftime("%D") if groupby_field_id.ttype in ['datetime', 'date'] else record.get(
                                groupby_field_id.name)
                            if not any(d['label'] == label_name for d in chart_data_list):
                                chart_data_list.append(
                                    {'label': label_name,
                                     'data': [record.get(operation_type) if label == label_name else 0],
                                     'fill': True})
                            else:
                                my_item = next((item for item in chart_data_list if item['label'] == label_name), None)
                                my_item.get('data').append(record.get(operation_type) if label == label_name else 0)

                dashboard.update({'line_chart_data': chart_data_list,
                                  'line_chart_labels': labels,
                                  'yAxes_labelString': 'Value',
                                  'xAxes_labelString': groupby_field_id.field_description, })
            elif dashboard['type'] in ['list']:
                order = ''
                if dashboard_id.sorting_field and dashboard_id.sorting_order:
                    order = '%s %s' % (dashboard_id.sorting_field.name, dashboard_id.sorting_order)
                if dashboard_id.list_type == 'non_group':
                    relation_fields_name = dashboard_id.list_view_fields.filtered(
                        lambda field: field.ttype in ['one2many', 'many2many', 'many2one']).mapped('name')
                    list_view_fields_name = dashboard_id.list_view_fields.mapped('name')
                    res = model_obj.search_read(safe_eval(dashboard['dashboard_domain']) + date_domain, list_view_fields_name, order=order, limit=dashboard['limit_record_count'])
                    for record in res:
                        record.pop('id')
                        for field in relation_fields_name:
                            record[field] = record.get(field) and record.get(field)[1] or ''

                    dashboard.update({'list_data': res,
                                      'list_technical_labels': list_view_fields_name,
                                      'list_labels': dashboard_id.list_view_fields.mapped('field_description'),
                                      'count_list_labels': len(dashboard_id.list_view_fields)})
                else:
                    relation_fields_name = (dashboard_id.list_view_groupby_fields + groupby_field_id).filtered(
                        lambda field: field.ttype in ['one2many', 'many2many', 'many2one']).mapped('name')
                    list_view_fields_name = dashboard_id.list_view_groupby_fields.mapped('name')
                    list_view_fields_groupby_field_name = Remove(list_view_fields_name + [groupby_field_id.name])
                    res = model_obj.read_group(domain=safe_eval(dashboard['dashboard_domain']) + date_domain,
                                               fields=list_view_fields_groupby_field_name,
                                               groupby=groupby_field_id.name,
                                               orderby=order,
                                               limit=dashboard['limit_record_count'])
                    list_view_data = []
                    for record in res:
                        record_dict = {}
                        for field in list(list_view_fields_groupby_field_name):
                            if field in relation_fields_name:
                                record_dict[field] = record.get(field)[1]
                            else:
                                record_dict[field] = record[field]
                        list_view_data.append(record_dict)
                    dashboard.update({'list_data': list_view_data,
                                      'list_technical_labels': list_view_fields_name,
                                      'list_labels': dashboard_id.list_view_groupby_fields.mapped('field_description') if groupby_field_id.field_description in dashboard_id.list_view_groupby_fields.mapped(
                                          'field_description') else dashboard_id.list_view_groupby_fields.mapped('field_description') + dashboard_id.groupby_field_id.mapped('field_description'),
                                      'count_list_labels': len(list_view_fields_groupby_field_name)})
        return dashboard_data

    def get_dashboard_data_for_form_view(self, dashboard_id):
        def Remove(duplicate):
            final_list = []
            for num in duplicate:
                if num not in final_list:
                    final_list.append(num)
            return final_list

        dashboard_data = {}
        date_domain = []
        groupby_field_id = dashboard_id.groupby_field_id
        is_relation_field = groupby_field_id.ttype == 'many2one'
        relation_field_obj = self.env[groupby_field_id.relation] if is_relation_field else False
        date_filter_field = dashboard_id.date_filter_field_id.name
        if dashboard_id.dashboard_model_name:
            model_obj = self.env[dashboard_id.dashboard_model_name]
            if dashboard_id.date_selection and date_filter_field:
                start_date, end_date = dashboard_id.get_date_range()
                date_domain = [(date_filter_field, '>=', fields.Date.to_string(start_date)),
                               (date_filter_field, '<=', fields.Date.to_string(end_date))]

            filtered_ids = model_obj.search(
                safe_eval(dashboard_id['dashboard_domain']) + date_domain)
            where_condition = ''
            if len(filtered_ids) == 1:
                where_condition = 'WHERE id = %s' % (filtered_ids.id)
            elif len(filtered_ids) > 1:
                where_condition = 'WHERE id in {}'.format(tuple(filtered_ids.ids))

            if dashboard_id.date_selection and date_filter_field and not where_condition:
                return {}

            if dashboard_id['type'] == 'tile':
                self.prepare_data_for_tile_form_renderer(dashboard_id, filtered_ids, where_condition, dashboard_data=dashboard_data)

            elif dashboard_id['type'] in ['line', 'bar', 'pie', 'polarArea'] and dashboard_id.operation_type and dashboard_id.measure_field_id:
                res = dashboard_id.get_chart_data(groupby_field_id, dashboard_id, where_condition)
                chart_data_list = []
                operation_type = dashboard_id.operation_type.lower()
                res = sorted([d for d in res if all(d.values())], key=lambda i: i[groupby_field_id.name])

                labels = [r[groupby_field_id.name].strftime("%D") if groupby_field_id.ttype in ['datetime','date'] else r[groupby_field_id.name] for r in res]
                if is_relation_field:
                    labels = [record.name for record in relation_field_obj.browse(labels)]

                if dashboard_id['type'] in ['pie', 'polarArea']:
                    chart_data_list.append({'data': [r[operation_type] for r in res]})
                else:
                    for record in res:
                        for label in labels:
                            label_name = relation_field_obj.browse(record.get(groupby_field_id.name)).name if is_relation_field else record.get(groupby_field_id.name).strftime("%D") if groupby_field_id.ttype in ['datetime', 'date'] else record.get(
                                groupby_field_id.name)
                            if not any(d['label'] == label_name for d in chart_data_list):
                                chart_data_list.append(
                                    {'label': label_name,
                                     'data': [record.get(operation_type) if label == label_name else 0],
                                     'fill': True})
                            else:
                                my_item = next((item for item in chart_data_list if item['label'] == label_name), None)
                                my_item.get('data').append(record.get(operation_type) if label == label_name else 0)

                dashboard_data.update({'line_chart_data': chart_data_list,
                                  'line_chart_labels': labels,
                                  'yAxes_labelString': 'Value',
                                  'xAxes_labelString': groupby_field_id.field_description, })
            elif dashboard_id['type'] in ['list']:
                order = ''
                if dashboard_id.sorting_field and dashboard_id.sorting_order:
                    order = '%s %s' % (dashboard_id.sorting_field.name, dashboard_id.sorting_order)
                if dashboard_id.list_type == 'non_group' and dashboard_id.list_view_fields:
                    relation_fields_name = dashboard_id.list_view_fields.filtered(
                        lambda field: field.ttype in ['one2many', 'many2many', 'many2one']).mapped('name')
                    date_fields_name = dashboard_id.list_view_fields.filtered(
                        lambda field: field.ttype in ['datetime', 'date']).mapped('name')
                    list_view_fields_name = dashboard_id.list_view_fields.mapped('name')
                    res = model_obj.search_read(safe_eval(dashboard_id['dashboard_domain']) + date_domain, list_view_fields_name, order=order, limit=dashboard_id['limit_record_count'])
                    for record in res:
                        record.pop('id')
                        for field in relation_fields_name:
                            record[field] = record.get(field) and record.get(field)[1] or ''
                        for date_field in date_fields_name:
                            record[date_field] = record[date_field].strftime("%D %T") if record[date_field] else ''

                    dashboard_data.update({'list_data': res,
                                      'list_technical_labels': list_view_fields_name,
                                      'list_labels': dashboard_id.list_view_fields.mapped('field_description'),
                                      'count_list_labels': len(dashboard_id.list_view_fields)})
                elif dashboard_id.list_type == 'group' and dashboard_id.list_view_groupby_fields and dashboard_id.groupby_field_id:
                    relation_fields_name = (dashboard_id.list_view_groupby_fields + groupby_field_id).filtered(
                        lambda field: field.ttype in ['one2many', 'many2many', 'many2one']).mapped('name')
                    list_view_fields_name = dashboard_id.list_view_groupby_fields.mapped('name')
                    list_view_fields_groupby_field_name = Remove(list_view_fields_name + [groupby_field_id.name])
                    res = model_obj.read_group(domain=safe_eval(dashboard_id['dashboard_domain']) + date_domain,
                                               fields=list_view_fields_groupby_field_name,
                                               groupby=groupby_field_id.name,
                                               orderby=order,
                                               limit=dashboard_id['limit_record_count'])
                    list_view_data = []
                    for record in res:
                        record_dict = {}
                        for field in list(list_view_fields_groupby_field_name):
                            if field in relation_fields_name:
                                record_dict[field] = record.get(field)[1]
                            else:
                                record_dict[field] = record[field]
                        list_view_data.append(record_dict)
                    dashboard_data.update({'list_data': list_view_data,
                                      'list_technical_labels': list_view_fields_name,
                                      'list_labels': dashboard_id.list_view_groupby_fields.mapped('field_description') if groupby_field_id.field_description in dashboard_id.list_view_groupby_fields.mapped(
                                          'field_description') else dashboard_id.list_view_groupby_fields.mapped('field_description') + dashboard_id.groupby_field_id.mapped('field_description'),
                                      'count_list_labels': len(list_view_fields_groupby_field_name)})
        return dashboard_data

    @api.depends('type', 'operation_type', 'dashboard_model_id', 'measure_field_id', 'date_filter_field_id', 'date_selection',
                 'groupby_field_id', 'list_type', 'list_view_fields', 'sorting_field', 'sorting_order', 'limit_record_count')
    def get_chart_data_form_preview(self):
        for rec in self:
            if rec.type in ['pie', 'bar', 'line']:
                chart_data = self.get_dashboard_data_for_form_view(rec)
                if chart_data:
                    try:
                        #TODO: Need to solve issue while selecting Date type field in Groupby field.
                        rec.chart_data = json.dumps(
                        {'labels': chart_data.get('line_chart_labels'), 'datasets': chart_data.get('line_chart_data'), 'yAxes_labelString': chart_data.get('yAxes_labelString'), 'xAxes_labelString': chart_data.get('xAxes_labelString')})
                    except:
                        rec.chart_data = False
                else:
                    rec.chart_data = {}
            elif rec.type in ['tile', 'list']:
                chart_data = self.get_dashboard_data_for_form_view(rec)
                rec.chart_data = json.dumps(chart_data)
            else:
                rec.chart_data = {}


    @api.multi
    def action_moveto_board(self):
        self.ensure_one()
        return {
            'name': _('Move To Board'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'move.to.board',
            'target': 'new',
        }