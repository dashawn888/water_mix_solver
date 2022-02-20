# Water/Juice Puzzle Solver

If you have ever played a water solver puzzle like this [Juice Sort Puzzle!](https://play.google.com/store/apps/details?id=com.SketchFalcon.Squid.Antistress.Relaxing.Water.Sort.Puzzle.Color.Sorting.Juice&hl=en_US&gl=US) then you know how much fun it is.

This is an algorithm to solve a level.

It works off the concept of always having an empty vial.  It goes through all possible moves until it findes a set of moves that creates an empty vial. It then repeats the task with the next configuration.

To build your level place all the vials into the main.py original_vials.

    original_vials = [
        Vial(0, [DG, BR, TU, GR]),
        Vial(1, [PU, PU, LG]),
        Vial(2, [FO, AQ, LG]),
        Vial(3, [FO, TU, PE, AQ]),
        Vial(4, [BL, BL, AQ, LG]),
        Vial(5, [BR, DG, BR, FO]),
        Vial(6, [PE]),
        Vial(7, [BL, TU, DG, BL]),
        Vial(8, [FO, GR]),
        Vial(9, [DG, GR, PE]),
        Vial(10, [PE, PU, BR, GR]),
        Vial(11, [TU, PU, LG, AQ]),
    ]
