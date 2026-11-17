"""Literal decay-display contracts, written before the producer."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np
path=Path(__file__).with_name("decay_figure_typography_20261117.py")
spec=importlib.util.spec_from_file_location("decay_typography",path)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class DecayDisplayContracts(unittest.TestCase):
    def test_preserves_both_saved_points_bands_and_reference(self):
        prediction={"lower":"-1.4","upper":"-.88"}
        rows=[{"n":448,"runtime_delta":.012,"contrast_per_delta":-1.19,
               "simultaneous_95_per_delta":[-1.25,-1.13],"response_contrast_per_delta":prediction},
              {"n":384,"runtime_delta":.022,"contrast_per_delta":-1.1,
               "simultaneous_95_per_delta":[-1.15,-1.05],"response_contrast_per_delta":prediction}]
        fig,axis=module.decay_figure(rows)
        self.assertEqual(len(axis.containers),1)
        x,y=axis.containers[0].lines[0].get_data()
        np.testing.assert_array_equal(x,[.012,.022])
        np.testing.assert_array_equal(y,[-1.19,-1.1])
        self.assertEqual(len(axis.patches),1)
        np.testing.assert_array_equal(axis.lines[0].get_ydata(),[0,0])
        text=[t.get_text() for t in axis.get_legend().get_texts()]
        self.assertTrue(any("unknown remainder" in t for t in text))
        self.assertTrue(any("approx." in t and "95%" in t for t in text))
        width,height=fig.get_size_inches()
        self.assertAlmostEqual(width,11.9/2.54)
        self.assertAlmostEqual(height/width,3.5/7.2)
        module.helper.assert_fonts_and_bounds(fig)
        for t in module.helper.drawn_texts(fig): self.assertGreaterEqual(t.get_fontsize(),8.5)
        module.helper.plt.close(fig)

if __name__=="__main__": unittest.main()
