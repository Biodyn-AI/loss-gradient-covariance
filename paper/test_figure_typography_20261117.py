"""Literal display contracts; no data-generation or random-number calls."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np
from matplotlib.text import Text

SOURCE=Path(__file__).with_name("figure_typography_20261117.py")
spec=importlib.util.spec_from_file_location("jota_typography",SOURCE)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def table_fixture():
    rows=[]
    for eta in (.001,.0002,.00004):
        methods={}
        for method in ("AdamW","SGD"):
            methods[method]={}
            for law in ("independent","coupled","matching","opposite"):
                point=.2 if law in ("coupled","matching") else .05
                methods[method][law]={"risk":point,"risk_per_eta":point,
                    "simultaneous_95":[.19,.21] if point==.2 else [.04,.06],"percentile_95":[.18,.22] if point==.2 else [.03,.07]}
            methods[method]["opposite_over_matching"]={"point":.55 if method=="AdamW" else 1.,
                "percentile_95":[.54,.56] if method=="AdamW" else [.999,1.001]}
        rows.append({"eta":eta,"methods":methods})
    return rows

class DisplayContracts(unittest.TestCase):
    def test_saved_series_keeps_every_point_and_correct_interval(self):
        eta,point,band=module.risk_series(table_fixture(),"AdamW","independent","risk","simultaneous_95")
        np.testing.assert_array_equal(eta,[.001,.0002,.00004])
        np.testing.assert_array_equal(point,[.05,.05,.05])
        np.testing.assert_array_equal(band,[[.04,.06]]*3)
    def test_matrix_keeps_four_full_clouds_and_inset(self):
        clouds=[np.vstack((np.linspace(-.01,.01,256),np.linspace(.01,-.01,256))) for _ in range(4)]
        clouds[1]=clouds[1]*40
        fig,axes,inset=module.matrix_figure(table_fixture(),clouds)
        self.assertEqual([len(c.get_offsets()) for c in axes[1].collections],[256]*4)
        self.assertEqual([len(c.get_offsets()) for c in inset.collections],[256]*3)
        self.assertEqual(len(axes[0].containers),4)
        self.check_geometry_and_fonts(fig,4.1/9)
        module.plt.close(fig)
    def test_scalar_keeps_four_curves_two_ratios_and_three_oracle_bands(self):
        oracle={"risk_per_eta":[{"lower":".18","upper":".22"},{"lower":".04","upper":".06"}],
                "anti_over_com_risk":{"lower":".47","upper":".63"}}
        fig,axes=module.scalar_figure(table_fixture(),oracle)
        self.assertEqual(len(axes[0].containers),4)
        self.assertEqual(len(axes[1].containers),2)
        self.assertEqual(len(axes[0].patches),2)
        self.assertEqual(len(axes[1].patches),1)
        self.check_geometry_and_fonts(fig,4.2/10)
        module.plt.close(fig)
    def check_geometry_and_fonts(self,fig,ratio):
        width,height=fig.get_size_inches()
        self.assertAlmostEqual(width,11.9/2.54)
        self.assertAlmostEqual(height/width,ratio)
        fig.canvas.draw()
        renderer=fig.canvas.get_renderer()
        bounds=fig.bbox
        for text in module.drawn_texts(fig):
            if text.get_visible() and text.get_text():
                self.assertGreaterEqual(text.get_fontsize(),8)
                bbox=text.get_window_extent(renderer)
                self.assertGreaterEqual(bbox.x0,bounds.x0-1)
                self.assertLessEqual(bbox.x1,bounds.x1+1)
                self.assertGreaterEqual(bbox.y0,bounds.y0-1)
                self.assertLessEqual(bbox.y1,bounds.y1+1)

if __name__=="__main__": unittest.main()
