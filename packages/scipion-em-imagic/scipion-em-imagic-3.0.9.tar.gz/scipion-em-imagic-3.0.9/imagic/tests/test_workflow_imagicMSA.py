# **************************************************************************
# *
# * Authors:     J.M. de la Rosa Trevin (jmdelarosa@cnb.csic.es)
# *              Grigory Sharov (gsharov@mrc-lmb.cam.ac.uk)
# *
# * Unidad de  Bioinformatica of Centro Nacional de Biotecnologia , CSIC
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 3 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************

from pwem.protocols import ProtImportParticles
from pyworkflow.tests import setupTestProject, DataSet
from pyworkflow.utils import magentaStr
from pwem.tests.workflows.test_workflow import TestWorkflow

from ..protocols import ImagicProtMSA, ImagicProtMSAClassify

   
class TestImagicWorkflow(TestWorkflow):
    @classmethod
    def setUpClass(cls):    
        setupTestProject(cls)
        cls.dataset = DataSet.getDataSet('mda')
        cls.particlesFn = cls.dataset.getFile('particles/xmipp_particles.xmd')
    
    def test_msaWorkflow(self):
        """ Run an Import particles protocol. """
        print(magentaStr("\n==> Importing data - particles:"))
        protImport = self.newProtocol(ProtImportParticles,
                                      importFrom=2,
                                      mdFile=self.particlesFn,
                                      samplingRate=3.5)
        self.launchProtocol(protImport)
        self.assertIsNotNone(protImport.outputParticles,
                             "SetOfParticles has not been produced.")

        print(magentaStr("\n==> Testing imagic - msa:"))
        protMsa = self.newProtocol(ImagicProtMSA,
                                   objLabel='imagic - msa',
                                   numberOfFactors=10,
                                   numberOfIterations=5,
                                   numberOfMpi=1)
        protMsa.inputParticles.set(protImport.outputParticles)
        self.launchProtocol(protMsa)

        print(magentaStr("\n==> Testing imagic - msa classify:"))
        protMsaClassify = self.newProtocol(ImagicProtMSAClassify,
                                           objLabel='imagic - msa classify',
                                           numberOfFactors=5,
                                           numberOfClasses=4)
        protMsaClassify.inputMSA.set(protMsa)
        self.launchProtocol(protMsaClassify)
        self.assertIsNotNone(protMsaClassify.outputClasses,
                             "There was a problem with the MSA-classify protocol's "
                             "outputClasses")
