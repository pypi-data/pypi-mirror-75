import os,sys,json
import numpy as np
import socket
import time
import logging

from .process import MPIWorker, MPIMaster
from ..util.timeline import Timeline, timeline

class MPISingleWorker(MPIWorker):
    """This class trains its model with no communication to other processes"""
    def __init__(self, num_epochs, data, algo, model_builder,
                verbose, monitor, custom_objects,
                early_stopping, target_metric,
                checkpoint, checkpoint_interval):

        self.has_parent = False

        self.best_val_loss = None
        self.target_metric = (target_metric if type(target_metric)==tuple else tuple(map(lambda s : float(s) if s.replace('.','').isdigit() else s, target_metric.split(',')))) if target_metric else None
        self.patience = (early_stopping if type(early_stopping)==tuple else tuple(map(lambda s : float(s) if s.replace('.','').isdigit() else s, early_stopping.split(',')))) if early_stopping else None
        
        logging.info("Creating MPISingleWorker")
            
        super(MPISingleWorker, self).__init__(data, algo, model_builder, process_comm=None, parent_comm=None, parent_rank=None, 
            num_epochs=num_epochs, verbose=verbose, monitor=monitor, custom_objects=custom_objects,
            checkpoint=checkpoint, checkpoint_interval=checkpoint_interval)

    def train(self):
        Timeline.begin("train")
        self.start_time = time.time()
        self.check_sanity()

        for epoch in range(1, self.num_epochs + 1):
            logging.info("beginning epoch {:d}".format(self.epoch + epoch))
            Timeline.begin("epoch")
            if self.monitor:
                self.monitor.start_monitor()
            epoch_metrics = np.zeros((1,))
            i_batch = 0

            for i_batch, batch in enumerate(self.data.generate_data()):
                Timeline.begin("train_on_batch")
                train_metrics = self.model.train_on_batch( x=batch[0], y=batch[1] )
                Timeline.end("train_on_batch")
                if epoch_metrics.shape != train_metrics.shape:
                    epoch_metrics = np.zeros( train_metrics.shape)
                epoch_metrics += train_metrics

                ######
                self.update = self.algo.compute_update( self.weights, self.model.get_weights() )
                if self.algo.mode == 'gem':
                    self.update = self.algo.compute_update_worker(self.weights, self.update)

                self.weights = self.algo.apply_update( self.weights, self.update )
                self.algo.set_worker_model_weights( self.model, self.weights )
                ######

                if self._short_batches and i_batch>self._short_batches: break

            if self.monitor:
                self.monitor.stop_monitor()
            epoch_metrics = epoch_metrics / float(i_batch+1)
            l = self.model.get_logs( epoch_metrics )
            self.update_history( l )

            Timeline.begin("epoch")

            if self.stop_training:
                break

            self.validate()
            self.save_checkpoint()
            

        logging.info("Signing off")
        if self.monitor:
            self.update_monitor( self.monitor.get_stats() )        

        self.stop_time = time.time()
        Timeline.end("train")
        self.data.finalize()

    def validate(self):
        return MPIMaster.validate_aux(self, self.weights, self.model)

    def record_details(self, json_name=None, meta=None):
        MPIMaster.record_details(self, json_name, meta)
